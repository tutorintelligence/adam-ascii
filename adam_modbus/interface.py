import asyncio
import socket
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Literal, assert_never


class AdamConnectionError(RuntimeError):
    pass


DEFAULT_ADAM_PORT = 1025
ADAM_CONNECTION_TIMEOUT = 0.1


@asynccontextmanager
async def adam_socket_context(
    ip: str,
    port: int = DEFAULT_ADAM_PORT,
) -> AsyncIterator[socket.socket]:
    adam_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    loop = asyncio.get_running_loop()

    # according to chatgpt, asyncio does not support timeouts on UDP sockets
    # so we manually do this with asyncio.wait_for, otherwise it will hang forever
    adam_sock.setblocking(False)

    try:
        await loop.sock_connect(adam_sock, (ip, port))
        yield adam_sock

    except OSError:
        raise AdamConnectionError(f"Could not connect to ADAM at {ip}")

    finally:
        adam_sock.close()


async def _adam_send_and_receive(message: str, adam_socket: socket.socket) -> str:
    loop = asyncio.get_running_loop()

    try:
        await asyncio.wait_for(
            loop.sock_sendall(adam_socket, message.encode("ascii")),
            ADAM_CONNECTION_TIMEOUT,
        )
        adam_out = await asyncio.wait_for(
            loop.sock_recv(adam_socket, 100), ADAM_CONNECTION_TIMEOUT
        )
    except asyncio.TimeoutError:
        raise AdamConnectionError("ADAM connection timed out")

    response = adam_out.decode().strip()
    return response


async def set_adam_digital_out(
    socket: socket.socket,
    model: Literal["6052"] | Literal["6317"],
    pin: int,
    value: bool,
) -> None:
    if model == "6052":
        command = f"#011{pin:x}0{int(value)}\r"
    elif model == "6317":
        command = f"#01D0{pin:x}{int(value)}\r"
    else:
        assert_never(model)

    response = await _adam_send_and_receive(command, socket)
    assert response[:3] == ">01", response[:3]


async def get_adam_digital_inputs(socket: socket.socket) -> list[bool]:
    response = await _adam_send_and_receive("$016\r", socket)
    assert response[:3] == "!01", f"Unexpected response: {response}"

    binary_string = "".join(f"{int(char, 16):0>4b}" for char in response[3:])
    return [char == "1" for char in binary_string][::-1]


async def get_adam_analog_inputs(socket: socket.socket) -> list[float]:
    response = await _adam_send_and_receive("#01\r", socket)

    assert response[:3] == ">01", response
    response_data = response[3:]

    # 7 characters per channel: +00.011
    assert len(response_data) % 7 == 0, response_data

    return [
        float(response_data[i * 7 : i * 7 + 7]) for i in range(len(response_data) // 7)
    ]


async def get_adam_model(socket: socket.socket) -> str:
    response = await _adam_send_and_receive("$01M\r", socket)

    assert response[:3] == "!01", f"Unexpected response: {response}"

    return response[3:]
