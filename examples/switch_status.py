


def get_switch_status():
    req = SwitchGetStatusRequest(
        id=1,
        params=SwitchGetStatusParams(id=0)
    )
    response = post(device_rpc_url, json=req.model_dump())
    # pprint(response.json()["result"])
    return response.json()["result"]


    SwitchStatus(**response.json()["result"])