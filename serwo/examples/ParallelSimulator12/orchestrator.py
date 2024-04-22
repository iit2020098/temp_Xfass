import logging
import json
import azure.functions as func
import azure.durable_functions as df
from .python.src.utils.classes.commons.serwo_objects import build_serwo_object
from .python.src.utils.classes.commons.serwo_objects import SerWOObject
import time
import os
import psutil
import uuid
import cpuinfo
import random
import string
from datetime import datetime, timedelta


def generate_random_string(N):
    res = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase +
                                 string.digits, k=N))

    return res


def trace_containers(metadata):
    function_id = 0
    container_path = "/tmp/serwo/container.txt"
    if not os.path.exists(container_path):
        os.mkdir("/tmp/serwo")
        f = open(container_path, "w")
        uuid_gen = str(uuid.uuid4())
        metadata[uuid_gen] = {}
        f.write(uuid_gen)
        f.close()
        if uuid_gen in metadata:
            uuid_map = metadata[uuid_gen]
            workflow_instance_id = str(metadata["workflow_instance_id"])
            if workflow_instance_id in uuid_map:
                metadata[uuid_gen][workflow_instance_id].append(function_id)
            else:
                metadata[uuid_gen][workflow_instance_id] = []
                metadata[uuid_gen][workflow_instance_id].append(function_id)
        else:
            metadata[uuid_gen] = {}
            workflow_instance_id = str(metadata["workflow_instance_id"])

            metadata[uuid_gen][workflow_instance_id] = []
            metadata[uuid_gen][workflow_instance_id].append(function_id)
    else:
        f = open(container_path, "r")
        saved_uuid = f.read()
        f.close()
        if saved_uuid in metadata:
            workflow_instance_id = metadata["workflow_instance_id"]
            if workflow_instance_id in metadata[saved_uuid]:
                metadata[saved_uuid][workflow_instance_id].append(function_id)
            else:
                metadata[saved_uuid][workflow_instance_id] = []
                metadata[saved_uuid][workflow_instance_id].append(function_id)
        else:

            metadata[saved_uuid] = {}
            workflow_instance_id = metadata["workflow_instance_id"]
            metadata[saved_uuid][workflow_instance_id] = []
            metadata[saved_uuid][workflow_instance_id].append(function_id)


def get_delta(start_time):
    curr_time = int(time.time() * 1000)
    return curr_time - start_time


def unmarshall(serwoObject):
    inp_dict = dict()
    if "_body" in serwoObject:
        inp_dict["body"] = serwoObject["_body"]
    if "_metadata" in serwoObject:
        inp_dict["metadata"] = serwoObject["_metadata"]
    if "_err" in serwoObject:
        inp_dict["error"] = serwoObject["_err"]
    serwoObject = build_serwo_object(inp_dict)
    return serwoObject


def insert_end_stats_in_metadata(input):
    serwoObjectJson = json.loads(input)
    serwoObjectJson = unmarshall(serwoObjectJson)
    metadata = serwoObjectJson.get_metadata()
    end_delta = get_delta(metadata["workflow_start_time"])
    meta_list = metadata["functions"]
    ne_list = []

    for meta in meta_list:
        start_delta_local = 0
        end_delta_local = 0
        func_id_local = 0
        mem_before = 0
        mem_after = 0
        body_size_before = 0
        body_size_after = 0
        cid = ''
        for fid in meta:
            func_id_local = fid
            start_delta_local = meta[fid]["start_delta"]
            end_delta_local = meta[fid]["end_delta"]
            if "mem_before" in meta[fid]:
                mem_before = meta[fid]["mem_before"]
                mem_after = meta[fid]["mem_after"]
                body_size_before = meta[fid]["in_payload_bytes"]
                body_size_after = meta[fid]["out_payload_bytes"]
                cid = meta[fid]["cid"]
            if fid == "0":
                end_delta_local = end_delta
        func_json = {
            func_id_local: {
                "start_delta": start_delta_local,
                "end_delta": end_delta_local,
                "mem_before": mem_before,
                "mem_after": mem_after,
                "in_payload_bytes": body_size_before,
                "out_payload_bytes": body_size_after,
                "cid": cid
            }
        }
        ne_list.append(func_json)
    body = serwoObjectJson.get_body()
    out_dict = dict()
    out_dict["body"] = body
    metadata["functions"] = ne_list
    out_dict["metadata"] = metadata
    input = build_serwo_object(out_dict).to_json()
    return input


def orchestrator_function(context: df.DurableOrchestrationContext):
    # convert input body to serwoObject for first function
    curr_time = int(time.time() * 1000)
    context_input = context.get_input()
    inp_dict = dict()
    inp_dict["body"] = context_input["body"]
    metadata = context_input["metadata"]
    request_timestamp = int(metadata["request_timestamp"])

    if "workflow_start_time" not in metadata:
        metadata["workflow_start_time"] = curr_time
    if "overheads" not in metadata:
        metadata["overheads"] = curr_time - request_timestamp
    if "request_timestamp" not in metadata:
        metadata["request_timestamp"] = request_timestamp
    func_id = 255

    start_delta = get_delta(metadata["workflow_start_time"])
    process = psutil.Process(os.getpid())
    memory = process.memory_info().rss
    metadata["init_orch_memory"] = memory
    end_delta = get_delta(metadata["workflow_start_time"])
    func_json = {func_id: {"start_delta": start_delta, "end_delta": end_delta}}
    metadata["functions"].append(func_json)
    inp_dict["metadata"] = metadata

    serwoObject = build_serwo_object(inp_dict).to_json()
    # user dag execution
    ghfl = yield context.call_activity("Splitter", serwoObject)
    bfis = yield context.call_activity("Transpiler8", ghfl)
    zfkg = yield context.call_activity("Transpiler10", ghfl)
    pjzs = yield context.call_activity("Transpiler1", ghfl)
    wsge = yield context.call_activity("Transpiler3", ghfl)
    osnt = yield context.call_activity("Transpiler9", ghfl)
    ajav = yield context.call_activity("Transpiler0", ghfl)
    bshi = yield context.call_activity("Transpiler5", ghfl)
    bfsn = yield context.call_activity("Transpiler4", ghfl)
    vyut = yield context.call_activity("Transpiler2", ghfl)
    hhhr = yield context.call_activity("Transpiler11", ghfl)
    cgxn = yield context.call_activity("Transpiler6", ghfl)
    gsrb = yield context.call_activity("Transpiler7", ghfl)
    qlnh = []
    nbbl = context.call_activity("Simulator8", bfis)
    iubg = context.call_activity("Simulator10", zfkg)
    hnaw = context.call_activity("Simulator1", pjzs)
    vjmk = context.call_activity("Simulator3", wsge)
    pyxi = context.call_activity("Simulator9", osnt)
    sdmt = context.call_activity("Simulator0", ajav)
    vzvu = context.call_activity("Simulator5", bshi)
    zpfu = context.call_activity("Simulator4", bfsn)
    jclm = context.call_activity("Simulator2", vyut)
    fvdt = context.call_activity("Simulator11", hhhr)
    owre = context.call_activity("Simulator6", cgxn)
    svhx = context.call_activity("Simulator7", gsrb)
    qlnh.append(nbbl)
    qlnh.append(iubg)
    qlnh.append(hnaw)
    qlnh.append(vjmk)
    qlnh.append(pyxi)
    qlnh.append(sdmt)
    qlnh.append(vzvu)
    qlnh.append(zpfu)
    qlnh.append(jclm)
    qlnh.append(fvdt)
    qlnh.append(owre)
    qlnh.append(svhx)
    gzjx = yield context.task_all(qlnh)
    zmkl = yield context.call_activity("Reconstructor", gzjx)
    zmkl = insert_end_stats_in_metadata(zmkl)
    xdif = yield context.call_activity("CollectLogs", zmkl)
    return xdif


main = df.Orchestrator.create(orchestrator_function)
