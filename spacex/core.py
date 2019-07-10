import discord

from redbot.core.utils.chat_formatting import humanize_timedelta

import aiohttp

from typing import Optional
from datetime import datetime

SPACE_X_API_BASE_URL = "https://api.spacexdata.com/v3/"


class Core:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def _unix_convert(self, timestamp: int):
        """Convert a unix timestamp to a readable datetime."""
        try:
            given = timestamp[: timestamp.find(".")] if "." in str(timestamp) else timestamp
            convert = datetime.utcfromtimestamp(int(given)).strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, OverflowError):
            raise ValueError(f"{given} is not a valid timestamp.")
        b = datetime.fromtimestamp(int(given))
        curr = datetime.fromtimestamp(int(datetime.now().timestamp()))
        secs = str((curr - b).total_seconds())
        seconds = secs[1:][:-2] if "-" in secs else secs[:-2] if ".0" in secs else secs
        delta = humanize_timedelta(seconds=int(seconds))
        return convert, delta

    async def _get_data(self, ctx, endpoint: Optional[str] = ""):
        """Get data from SpaceX API."""
        async with self.session.get(SPACE_X_API_BASE_URL + endpoint) as resp:
            if resp.status == 404:
                await ctx.send("It doesn't seem to be a valid request.")
                return None
            if resp.status != 200:
                await ctx.send(
                    "Error when trying to get SpaceX API. Error code: `{}`".format(resp.status)
                )
                return None
            data = await resp.json()
            return data

    async def _about(self, ctx):
        async with ctx.typing():
            data = await self._get_data(ctx, "info")
            if data is None:
                return

            spacex_infos_kwargs = {
                "founder": data["founder"],
                "ceo": data["ceo"],
                "coo": data["coo"],
                "cto": data["cto"],
                "founded": data["founded"],
                "headq_a": data["headquarters"]["address"],
                "headq_c": data["headquarters"]["city"],
                "headq_s": data["headquarters"]["state"],
            }
            spacex_stats_kwargs = {
                "employees": data["employees"],
                "vehicles": data["vehicles"],
                "launch_s": data["launch_sites"],
                "test_s": data["test_sites"],
                "value": data["valuation"],
                "web": data["links"]["website"],
                "flickr": data["links"]["flickr"],
                "twitter": data["links"]["twitter"],
                "elon_t": data["links"]["elon_twitter"],
            }
            spacex_infos = (
                "Founder: **{founder}**\n"
                "CEO and CTO: **{ceo}**\n"
                "COO: **{coo}**\n"
                "CTO: **{cto}**\n"
                "Founded: **{founded}**\n"
                "Headquarters: **{headq_a} {headq_c} {headq_s}**"
            ).format(**spacex_infos_kwargs)
            spacex_stats_links = (
                "Employees: **{employees}**\n"
                "Vehicles: **{vehicles}**\n"
                "Launch sites: **{launch_s}**\n"
                "Test sites: **{test_s}**\n"
                "Valuation: **{value:,}$**\n\n"
                "**[Website]({web})** • **[Flickr]({flickr})** • "
                "**[Twitter]({twitter})** • **[Elon Musk Twitter]({elon_t})**"
            ).format(**spacex_stats_kwargs)

            em = discord.Embed(
                color=await ctx.embed_colour(), title=data["name"], description=data["summary"]
            )
            em.add_field(name="Informations:", value=spacex_infos)
            em.add_field(name="Stats:", value=spacex_stats_links)
            em.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/514586665730441248/576130134046670869/5842a770a6515b1e0ad75afe.png"
            )
            return await ctx.send(embed=em)

    async def _about_cog(self, ctx, version=None):
        async with ctx.typing():
            data = await self._get_data(ctx)
            description = data["description"]
            docs = data["docs"]
            project_link = data["project_link"]
            if data is None:
                description = (
                    "Open Source REST API for rocket, core, capsule, pad, and launch data, "
                    "created and maintained by the developers of the r/SpaceX organization"
                )
                docs = "https://documenter.getpostman.com/view/2025350/RWaEzAiG"
                project_link = "https://github.com/r-spacex/SpaceX-API"
                return

            title_api = "About SpaceX-API:\n"
            title_cog = "About this cog:\n"
            desc_api = (
                description + "\n**[Docs]({docs})** • **[Project Link]({project})**"
            ).format(docs=docs, project=project_link)
            desc_cog = (
                f"Cog version: {version}\nYou can also use "
                "[Space cog from kennnyshiwa](https://github.com/kennnyshiwa/kennnyshiwa-cogs) "
                "for more about space in general, space pics, Astronomy Picture of the Day from Nasa, "
                "ISS location ..."
            )
            em = discord.Embed(color=await ctx.embed_colour())
            em.add_field(name=title_api, value=desc_api)
            em.add_field(name=title_cog, value=desc_cog)
        return await ctx.send(embed=em)

    async def _history_texts(self, data):
        description_kwargs = {
            "date": data["event_date_utc"].replace("T", " ")[:-1],
            "flight_num": "Flight number: **{}**\n".format(data["flight_number"])
            if data["flight_number"] is not None
            else "",
            "article": "[Article]({})".format(data["links"]["article"]),
            "wikipedia": " • [Wikipedia]({})".format(data["links"]["wikipedia"])
            if data["links"]["wikipedia"] is not None
            else "",
            "reddit": " • [Reddit]({})".format(data["links"]["reddit"])
            if data["links"]["reddit"] is not None
            else "",
        }
        description = (
            "Date: **{date}**\n" "{flight_num}" "Links: **{article}{wikipedia}{reddit}**"
        ).format(**description_kwargs)
        return description

    async def _launchpads_texts(self, data):
        description_kwargs = {
            "status": data["status"],
            "region": data["location"]["region"],
            "location": "Lat: {lat} • Long: {long}".format(
                lat=round(data["location"]["latitude"], 2),
                long=round(data["location"]["longitude"], 2),
            ),
            "site_id": data["site_id"],
            "att_launches": data["attempted_launches"],
            "succ_launches": data["successful_launches"],
            "s": "s" if len(data["vehicles_launched"]) >= 2 else "",
            "vehicles": ", ".join(data["vehicles_launched"]),
            "site_name_ext": data["site_name_long"],
        }
        description = (
            "Status: **{status}**\n"
            "Region: **{region}**\n"
            "Location: **{location}**\n"
            "Site ID: **{site_id}**\n"
            "Attempted launches: **{att_launches}**\n"
            "Success launches: **{succ_launches}**\n"
            "Vehicle{s} launched: **{vehicles}**\n"
            "Site name long: **{site_name_ext}**"
        ).format(**description_kwargs)
        return description

    async def _landpads_texts(self, data):
        description_kwargs = {
            "status": data["status"],
            "landing_t": data["landing_type"],
            "att_lands": data["attempted_landings"],
            "succ_lands": data["successful_landings"],
            "location": "{name} {region} • Lat: {lat} Long: {long}".format(
                name=data["location"]["name"],
                region=data["location"]["region"],
                lat=data["location"]["latitude"],
                long=data["location"]["longitude"],
            ),
        }
        description = (
            "Status: **{status}**\n"
            "Landing type: **{landing_t}**\n"
            "Attempted landings: **{att_lands}**\n"
            "Success landings: **{succ_lands}**\n"
            "Location: **{location}**"
        ).format(**description_kwargs)
        return description

    async def _missions_texts(self, data):
        description_kwargs = {
            "website": " • **[Website]({})**".format(data["website"])
            if data["website"] is not None
            else "",
            "twitter": " • **[Twitter]({})**".format(data["twitter"])
            if data["twitter"] is not None
            else "",
        }
        description = (
            data["description"]
            + "\n**[Wikipedia page]({})**".format(data["wikipedia"])
            + "{website}{twitter}"
        ).format(**description_kwargs)
        return description

    async def _roadster_texts(self, data):
        date, delta = await self._unix_convert(data["launch_date_unix"])
        roadster_stats_kwargs = {
            "launch_date": date,
            "ago": delta[:-31],
            "mass_kg": data["launch_mass_kg"],
            "mass_lbs": data["launch_mass_lbs"],
            "speed_km": round(data["speed_kph"], 2),
            "speed_mph": round(data["speed_mph"], 2),
            "e_distance_km": round(data["earth_distance_km"], 2),
            "e_distance_mi": round(data["earth_distance_mi"], 2),
            "m_distance_km": round(data["mars_distance_km"], 2),
            "m_distance_mi": round(data["mars_distance_mi"], 2),
        }
        roadster_stats = (
            "Launch date: **{launch_date} {ago} ago**\n"
            "Launch mass: **{mass_kg:,} kg / {mass_lbs:,} lbs**\n"
            "Actual speed: **{speed_km:,} km/h / {speed_mph:,} mph**\n"
            "Earth distance: **{e_distance_km:,} km / {e_distance_mi:,} mi**\n"
            "Mars distance: **{m_distance_km:,} km / {m_distance_mi:,} mi**\n"
        ).format(**roadster_stats_kwargs)
        return roadster_stats

    async def _rockets_texts(self, data):
        base_stats_kwargs = {
            "first_flight": data["first_flight"],
            "active": "Yes" if data["active"] is True else "No",
            "stages": data["stages"],
            "l_legs": data["landing_legs"]["number"],
            "success_rate": data["success_rate_pct"],
            "cost": data["cost_per_launch"],
            "m_height": round(data["height"]["meters"], 2),
            "f_height": round(data["height"]["feet"], 2),
            "m_diam": round(data["diameter"]["meters"], 2),
            "f_diam": round(data["diameter"]["feet"], 2),
            "kg_mass": round(data["mass"]["kg"], 2),
            "lb_mass": round(data["mass"]["lb"], 2),
            "engines": data["engines"]["number"],
            "e_type": data["engines"]["type"],
            "e_version": data["engines"]["version"],
        }
        base_stats = (
            "First flight: **{first_flight}**\n"
            "Active: **{active}**\n"
            "Stages: **{stages:,}**\n"
            "Landing legs: **{l_legs:,}**\n"
            "Success rate: **{success_rate}%**\n"
            "Cost per launch: **{cost:,}$**\n"
            "Height: **{m_height:,} m / {f_height:,} f**\n"
            "Diameter: **{m_diam:,} m / {f_diam:,} f**\n"
            "Mass: **{kg_mass:,} kg / {lb_mass:,} lbs**\n"
            "Engines: **{engines} {e_type} {e_version}**"
        ).format(**base_stats_kwargs)
        stages_stats_kwargs = {
            "fi_reusable": "Yes" if data["first_stage"]["reusable"] is True else "No",
            "fi_engines": data["first_stage"]["engines"],
            "fi_fuel_amount": data["first_stage"]["fuel_amount_tons"],
            "fi_burn_time": "N/A"
            if data["first_stage"]["burn_time_sec"] is None
            else data["first_stage"]["burn_time_sec"],
            "sec_reusable": "Yes" if data["second_stage"]["reusable"] is True else "No",
            "sec_engines": data["second_stage"]["engines"],
            "sec_fuel_amount": data["second_stage"]["fuel_amount_tons"],
            "sec_burn_time": "N/A"
            if data["second_stage"]["burn_time_sec"] is None
            else data["second_stage"]["burn_time_sec"],
        }
        stages_stats = (
            "***First stage:***\n"
            "Reusable: **{fi_reusable}**\n"
            "Engines: **{fi_engines}**\n"
            "Fuel amount: **{fi_fuel_amount} tons**\n"
            "Burn time: **{fi_burn_time} secs**\n"
            "***Second stage:***\n"
            "Reusable: **{sec_reusable}**\n"
            "Engines: **{sec_engines}**\n"
            "Fuel amount: **{sec_fuel_amount} tons**\n"
            "Burn time: **{sec_burn_time} secs**\n"
        ).format(**stages_stats_kwargs)
        payload_weights_stats = ""
        for p in data["payload_weights"]:
            payload_weights_stats += (
                "Name: **{p_name}**\n" "Weight: **{kg_mass:,} kg / {lb_mass:,} lbs**\n"
            ).format(p_name=p["name"], kg_mass=p["kg"], lb_mass=p["lb"])
        engines_stats_kwargs = {
            "number": data["engines"]["number"],
            "type": data["engines"]["type"],
            "version": "None" if data["engines"]["version"] == "" else data["engines"]["version"],
            "layout": data["engines"]["layout"],
            "p_1": data["engines"]["propellant_1"],
            "p_2": data["engines"]["propellant_2"],
        }
        engines_stats = (
            "Number: **{number:,}**\n"
            "Type: **{type}**\n"
            "Version: **{version}**\n"
            "Layout: **{layout}**\n"
            "Propellants: **{p_1} and {p_2}**"
        ).format(**engines_stats_kwargs)
        return base_stats, stages_stats, payload_weights_stats, engines_stats

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())
