import aiohttp_cors
from aiohttp import web
import asyncio
from ..database.db import Database

def create_dashboard_api_route(app):
    # CORS setup
    cors = aiohttp_cors.setup(app)

    # Will execute when route is hit
    @asyncio.coroutine
    def handler(request):
        db = Database()
        messages = db.get_all()
        return web.json_response(messages)

    # registering the route as a resource
    resource = cors.add(app.router.add_resource("/api"))

    # adding the route to cors
    cors.add(
        resource.add_route("GET", handler), {
            "http://localhost:3000": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers=("X-Custom-Server-Header",),
                allow_headers=("X-Requested-With", "Content-Type"),
                max_age=3600,
            )
        })


def setup_cors(app):
    # The `cors` instance will store CORS configuration for the
    # application.
    cors = aiohttp_cors.setup(app)

    # To enable CORS processing for specific route you need to add
    # that route to the CORS configuration object and specify its
    # CORS options.
    cors.add(app.router.add_resource("/api"), {
        "http://localhost:3000": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers=("X-Custom-Server-Header",),
            allow_headers=("X-Requested-With", "Content-Type"),
            max_age=3600,
            allow_methods=["GET"]
        )
    })

    # cors.add(app.router.add_resource("/api2"), {
    #     "http://localhost:3000": aiohttp_cors.ResourceOptions(
    #         allow_credentials=True,
    #         expose_headers=("X-Custom-Server-Header",),
    #         allow_headers=("X-Requested-With", "Content-Type"),
    #         max_age=3600,
    #         allow_methods=["GET"]
    #     )
    # })

    # cors.add(app.router.add_resource("/socket.io/"), {
    #     "http://localhost:3000": aiohttp_cors.ResourceOptions(
    #          allow_credentials=True,
    #          expose_headers=("X-Custom-Server-Header",),
    #          allow_headers=("X-Requested-With", "Content-Type"),
    #          max_age=3600,
    #          allow_methods=["GET"]
    #          )
    # })
