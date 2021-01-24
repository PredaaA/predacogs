# Basic setup for InfluxDB (with Docker & Docker Compose) on linux

## Docker and Docker Compose installation

Follow those guides provided directly by Docker:

- <https://docs.docker.com/engine/install/ubuntu/>
- <https://docs.docker.com/compose/install/>

## InfluxDB installation

> **For this guide, we are assuming that you don't already have data from an old instance.**

Let's say we have a folder named `docker/influxdb` on our user home folder.
Let's create an `docker-compose.yml` in our `influxdb` folder, and in that file copy the following:

```yml
version: "3.5"
services:
  influxdb:
    container_name: influxdb
    image: quay.io/influxdb/influxdb:2.0.3
    restart: always
    volumes:
      - /home/user/influxdbdata:/var/lib/influxdb2
    networks:
      influxdb-net:
        ipv4_address: 172.60.0.2
    ports:
      - 8086:8086
    command: influxd run --bolt-path /var/lib/influxdb2/influxd.bolt --engine-path /var/lib/influxdb2/engine --store bolt

networks:
  influxdb-net:
    name: influxdb-net
    driver: bridge
    ipam:
      config:
        - subnet: 172.60.0.0/16
```

So here we have a config for a Docker container, that will have its data persisting at path `/home/user/influxdbdata`, this can be anywhere on your host, it will be binded to a static IP which is `172.60.0.2`, and finally, it exposes port 8086 and will restart automatically on host reboots.

Start this container with `docker-compose up -d`.

Now that the container is up, by going to `host_ip:8086` you should see a web page, with a Get Started button, if so follow the instructions here <https://docs.influxdata.com/influxdb/v2.0/get-started/#set-up-influxdb-through-the-ui/>.

### Some basic commands

- To restart container with a new docker-compose config: `docker-compose up -d`
- To stop the container: `docker stop influxdb` or in your docker-compose file path `docker-compose stop`
- To see logs of your instance: `docker logs -n 100 -f influxdb` or in your docker-compose file path `docker-compose logs --tail 100 -f influxdb`
- To connect to the container console: `docker exec -it /bin/bash influxdb`

### Notes

For owner of 2.0.0-beta instances, [follow this guide to convert your old data](https://docs.influxdata.com/influxdb/v2.0/upgrade/v2-beta-to-v2).

**Warning:** Their convert process can be very resource intensive, and also take *a lot* of space, make sure you have enough space on your host before proceeding.

## Cog setup

Once your InfluxDB instance is set up, we can finally link TimeSeries cog to it.

```bash
[p]timeseriesset url localhost:8086
[p]timeseriesset bucket bucket_name
[p]timeseriesset org organization_name
[p]timeseriesset token bucket_token
```

Optional:

```bash
# Enabling this will store Top.gg stats of your bot
# (needs an Top.gg token)
[p]timeseriesset topggstats

# Enabling this will only send basic stats to influx, which
# will use a lot less resources.
[p]timeseriesset lightmode
```
