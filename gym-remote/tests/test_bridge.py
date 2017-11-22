import gym_remote as gr

from . import tempdir


def setup_client_server(base):
    server = gr.Bridge(base)
    server.listen()

    client = gr.Bridge(base)
    client.connect()
    return client, server


def start_bridge(client, server):
    server.server_accept()
    client.configure_client()


def test_bridge_setup_connection(tempdir):
    client, server = setup_client_server(tempdir)
    start_bridge(client, server)


def test_bridge_int(tempdir):
    client, server = setup_client_server(tempdir)
    server.add_channel('int', gr.IntChannel())

    start_bridge(client, server)

    assert list(server._channels.keys()) == ['int']
    assert list(client._channels.keys()) == ['int']

    assert server._channels['int'].value is None
    assert client._channels['int'].value is None

    server._channels['int'].value = 1
    server.send()
    client.recv()

    assert server._channels['int'].value == 1
    assert client._channels['int'].value == 1

    server._channels['int'].value = 2
    server.send()
    client.recv()

    assert server._channels['int'].value == 2
    assert client._channels['int'].value == 2


def test_bridge_float(tempdir):
    client, server = setup_client_server(tempdir)
    server.add_channel('float', gr.FloatChannel())

    start_bridge(client, server)

    assert list(server._channels.keys()) == ['float']
    assert list(client._channels.keys()) == ['float']

    assert server._channels['float'].value is None
    assert client._channels['float'].value is None

    server._channels['float'].value = 1
    server.send()
    client.recv()

    assert server._channels['float'].value == 1
    assert client._channels['float'].value == 1

    server._channels['float'].value = 0.5
    server.send()
    client.recv()

    assert server._channels['float'].value == 0.5
    assert client._channels['float'].value == 0.5


def test_bridge_bool(tempdir):
    client, server = setup_client_server(tempdir)
    server.add_channel('bool', gr.BoolChannel())

    start_bridge(client, server)

    assert list(server._channels.keys()) == ['bool']
    assert list(client._channels.keys()) == ['bool']

    assert server._channels['bool'].value is None
    assert client._channels['bool'].value is None

    server._channels['bool'].value = True
    server.send()
    client.recv()

    assert server._channels['bool'].value == True
    assert client._channels['bool'].value == True

    server._channels['bool'].value = False
    server.send()
    client.recv()

    assert server._channels['bool'].value == False
    assert client._channels['bool'].value == False


def test_bridge_int_fold(tempdir):
    client, server = setup_client_server(tempdir)
    server.add_channel('int_fold', gr.IntFoldChannel((2, 3)))

    start_bridge(client, server)

    assert list(server._channels.keys()) == ['int_fold']
    assert list(client._channels.keys()) == ['int_fold']

    assert server._channels['int_fold'].value is None
    assert client._channels['int_fold'].value is None

    server._channels['int_fold'].value = [1, 2]
    server.send()
    client.recv()

    assert server._channels['int_fold'].value == [1, 2]
    assert client._channels['int_fold'].value == [1, 2]

    server._channels['int_fold'].value = [0, 1]
    server.send()
    client.recv()

    assert server._channels['int_fold'].value == [0, 1]
    assert client._channels['int_fold'].value == [0, 1]


def test_bridge_np(tempdir):
    import numpy as np
    client, server = setup_client_server(tempdir)
    server.add_channel('np', gr.NpChannel((2, 2), int))

    start_bridge(client, server)

    assert list(server._channels.keys()) == ['np']
    assert list(client._channels.keys()) == ['np']

    server._channels['np'].value = np.zeros((2, 2), int)
    server.send()
    client.recv()

    assert (server._channels['np'].value == np.zeros((2, 2))).all()
    assert (client._channels['np'].value == np.zeros((2, 2))).all()

    server._channels['np'].value = np.ones((2, 2), int)
    server.send()
    client.recv()

    assert (server._channels['np'].value == np.ones((2, 2))).all()
    assert (client._channels['np'].value == np.ones((2, 2))).all()


def test_bridge_multi(tempdir):
    client, server = setup_client_server(tempdir)
    server.add_channel('int', gr.IntChannel())
    server.add_channel('bool', gr.BoolChannel())

    start_bridge(client, server)

    assert set(server._channels.keys()) == {'int', 'bool'}
    assert set(client._channels.keys()) == {'int', 'bool'}

    assert server._channels['int'].value is None
    assert client._channels['int'].value is None
    assert server._channels['bool'].value is None
    assert client._channels['bool'].value is None

    server._channels['bool'].value = True
    server.send()
    client.recv()

    assert server._channels['int'].value is None
    assert client._channels['int'].value is None
    assert server._channels['bool'].value == True
    assert client._channels['bool'].value == True

    server._channels['int'].value = 1
    server.send()
    client.recv()

    assert server._channels['int'].value is 1
    assert client._channels['int'].value is 1
    assert server._channels['bool'].value == True
    assert client._channels['bool'].value == True

    server._channels['bool'].value = False
    server._channels['int'].value = 2
    server.send()
    client.recv()

    assert server._channels['int'].value is 2
    assert client._channels['int'].value is 2
    assert server._channels['bool'].value == False
    assert client._channels['bool'].value == False
