import json


base_method = """from aiohttp import ClientSession


class BaseMethod:
    _session: ClientSession
    _token: str

    def __init__(self, token: str, session: ClientSession):
        self._token = token
        self._session = session
        
    async def request(self, **kwargs):
        return await self._session.post(
            "https://api.telegram.org/bot" + self._token + "/",
            json=kwargs,
        )
    
    async def __call__(self, **kwargs):
        return await self.request(**kwargs)
"""


def gen():
    with open("api.min.json", "r") as f:
        data = json.load(f)

    
    for ttype in data["types"].values():
        with open("tg/types/" + ttype["name"] + ".py", "w") as f:
            s = "from dataclasses import dataclass\n\n@dataclass\n"

            used_types = set()

            tname = ttype["name"]
            tdesc = "\n    ".join(ttype["description"]) if type(ttype[
                "description"]) == list else ttype["description"]

            if "subtype_of" in ttype:
                for st in ttype["subtype_of"]:
                    s = f"from .{st} import {st}\n" + s
                s += f"class {tname}({' | '.join(ttype['subtype_of'])}):\n"
            else:
                s += f"class {tname}:\n"
            
            s += f"    '''\n    {tdesc}\n    '''\n\n"
            
            if "fields" not in ttype:
                s += "    pass\n"
                f.write(s)
                continue
            
            for field in ttype["fields"]:
                fname = field["name"]
                ftypes = field["types"]
                frequired = field["required"]
                fdesc = "\n".join(field["description"]) if type(field["description"\
                    ]) == list else field["description"]

                if fname == 'from':
                    fname = 'from_'

                s += f"    {fname}: "

                ptype = ""

                for t in ftypes:
                    dtype = t
                    default = None

                    if "of" in t:
                        level = t.count("of")
                        btype = t.split(" ")[-1]

                        if btype == "Integer":
                            btype = "int"
                        elif btype == "Float":
                            btype = "float"
                        elif btype == "Boolean":
                            btype = "bool"
                        elif btype == "String":
                            btype = "str"
                        elif btype == "True":
                            default = "False"
                            btype = "bool"
                        else:
                            used_types.add(btype)

                        dtype = "list[" * level + btype + "]" * level
                    else:
                        if dtype == "Integer":
                            dtype = "int"
                        elif dtype == "Float":
                            dtype = "float"
                        elif dtype == "Boolean":
                            dtype = "bool"
                        elif dtype == "String":
                            dtype = "str"
                        elif dtype == "True":
                            dtype = "bool"
                        else:
                            used_types.add(dtype)
                    
                    ptype += dtype + " |"
                
                ptype = ptype[:-2]

                if not frequired:
                    if ptype == "bool":
                        default = "False"
                    else:
                        ptype += " | None"
                        default = "None"
                
                if default:
                    ptype += f" = {default}"
                
                s += ptype
                
                s += "\n"

                if type(fdesc) == list:
                    fdesc = "\n".join(fdesc)
                
                s += f"    '''\n    {fdesc}\n    '''\n\n"

                for ut in used_types:
                    s = f"from .{ut} import {ut}\n" + s
        
            f.write(s)

    
    for method in data["methods"].values():
        with open("tg/methods/" + method["name"] + ".py", "w") as f:
            s = "from .BaseMethod import BaseMethod\n\n"

            used_types = set()

            tname = method["name"]
            tdesc = "\n    ".join(method["description"]) if type(method[
                "description"]) == list else method["description"]

            s += f"class {tname}(BaseMethod):\n"
            s += f"    '''\n    {tdesc}\n    '''\n\n"
            s += f"    async def __call__(self,\n"
            
            if "fields" not in method:
                s = s[:-1] + "):\n"
                f.write(s)
            else:
                fields = []
                for i, field in enumerate(method["fields"]):
                    fname = field["name"]
                    ftypes = field["types"]
                    frequired = field["required"]
                    fdesc = "\n".join(field["description"]) if type(field["description"\
                        ]) == list else field["description"]

                    if fname == 'from':
                        fname = 'from_'

                    _s = f"    {fname}: "

                    ptype = ""

                    for t in ftypes:
                        dtype = t
                        default = None

                        if "of" in t:
                            level = t.count("of")
                            btype = t.split(" ")[-1]

                            if btype == "Integer":
                                btype = "int"
                            elif btype == "Float":
                                btype = "float"
                            elif btype == "Boolean":
                                btype = "bool"
                            elif btype == "String":
                                btype = "str"
                            elif btype == "True":
                                default = "False"
                                btype = "bool"
                            else:
                                used_types.add(btype)

                            dtype = "list[" * level + btype + "]" * level
                        else:
                            if dtype == "Integer":
                                dtype = "int"
                            elif dtype == "Float":
                                dtype = "float"
                            elif dtype == "Boolean":
                                dtype = "bool"
                            elif dtype == "String":
                                dtype = "str"
                            elif dtype == "True":
                                dtype = "bool"
                            else:
                                used_types.add(dtype)
                        
                        ptype += dtype + " |"
                    
                    ptype = ptype[:-2]

                    if not frequired:
                        if ptype == "bool":
                            default = "False"
                        else:
                            ptype += " | None"
                            default = "None"
                    
                    if default:
                        ptype += f" = {default}"
                    
                    method["fields"][i]["type"] = ptype.split("|")[0].strip()
                    
                    _s += ptype
                    
                    _s += ",\n"

                    if type(fdesc) == list:
                        fdesc = "\n".join(fdesc)
                    
                    if default:
                        fields.append(_s)
                    else:
                        fields = [_s, *fields]
                s += "".join(fields)
            
            if "returns" in method:
                rtype = ""
                for t in method["returns"]:
                    dtype = t
                    default = None

                    if "of" in t:
                        level = t.count("of")
                        btype = t.split(" ")[-1]

                        if btype == "Integer":
                            btype = "int"
                        elif btype == "Float":
                            btype = "float"
                        elif btype == "Boolean":
                            btype = "bool"
                        elif btype == "String":
                            btype = "str"
                        elif btype == "True":
                            default = "False"
                            btype = "bool"
                        else:
                            used_types.add(btype)

                        dtype = "list[" * level + btype + "]" * level
                    else:
                        if dtype == "Integer":
                            dtype = "int"
                        elif dtype == "Float":
                            dtype = "float"
                        elif dtype == "Boolean":
                            dtype = "bool"
                        elif dtype == "String":
                            dtype = "str"
                        elif dtype == "True":
                            dtype = "bool"
                        else:
                            used_types.add(dtype)
                    
                    rtype += dtype + " |"
                
                rtype = rtype[:-2]
            else:
                rtype = "None"
        
            s += "    ) -> " + rtype + ":\n"

            if "fields" in method:
                s += "        '''\n"
                for field in method["fields"]:
                    fname = field["name"]
                    fdesc = "\n".join(field["description"]) if type(field["description"\
                        ]) == list else field["description"]
                    s += f"        :param {fname}: {fdesc}\n"
                    s += f"        :type {fname}: {field['type']}\n"
                s += "        '''\n"

            s += "        return await self.request(\n"
            if "fields" in method:
                for field in method["fields"]:
                    fname = field["name"]
                    s += f"            {fname}={fname},\n"
                s += "        )\n"
            else:
                s = s[:-1] + ")\n"

            for ut in used_types:
                s = f"from ..types.{ut} import {ut}\n" + s

            f.write(s)
    
    with open("tg/methods/__init__.py", "w") as f:
        s = ""
        for method in data["methods"].values():
            s += f"from .{method['name']} import {method['name']}\n"
        s += "\n__all__ = (\n"
        for method in data["methods"].values():
            s += f"    '{method['name']}',\n"
        s += ")\n"
        f.write(s)
    
    with open("tg/types/__init__.py", "w") as f:
        s = ""
        for ttype in data["types"].values():
            s += f"from .{ttype['name']} import {ttype['name']}\n"
        s += "\n__all__ = (\n"
        for ttype in data["types"].values():
            s += f"    '{ttype['name']}',\n"
        s += ")\n"
        f.write(s)
    
    with open("tg/__init__.py", "w") as f:
        s = ""
        for ttype in data["types"].values():
            s += f"from .types.{ttype['name']} import {ttype['name']}\n"
        for method in data["methods"].values():
            s += f"from .methods.{method['name']} import {method['name']}\n"
        s += "\n__all__ = (\n"
        for ttype in data["types"].values():
            s += f"    '{ttype['name']}',\n"
        for method in data["methods"].values():
            s += f"    '{method['name']}',\n"
        s += ")\n"
        f.write(s)
    
    with open("tg/methods/BaseMethod.py", "w") as f:
        f.write(base_method)


if __name__ == "__main__":
    gen()
