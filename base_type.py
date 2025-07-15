from dataclasses import dataclass, is_dataclass
from typing import get_origin, get_args, List, Union, Any, get_type_hints
import inspect


def base_type(cls):
    annotations = getattr(cls, '__annotations__', {})
    
    for name, ann in annotations.items():
        origin = get_origin(ann)
        args = get_args(ann)
        
        if origin is Union and type(None) in args:
            if not hasattr(cls, name):
                setattr(cls, name, None)
    
    cls = dataclass(cls)
    original_init = cls.__init__
    
    def _process_value(value, field_type):
        if value is None:
            return value
            
        origin = get_origin(field_type)
        args = get_args(field_type)
        
        if origin is Union and type(None) in args:
            for t in args:
                if t is not type(None):
                    return _process_value(value, t)
            return value
        
        if origin in (list, List):
            item_type = args[0] if args else Any
            if isinstance(value, list):
                return [_process_value(item, item_type) for item in value]
            return [_process_value(value, item_type)]
        
        if inspect.isclass(field_type) and is_dataclass(field_type):
            if isinstance(value, dict):
                return field_type(**value)
            elif isinstance(value, field_type):
                return value
            else:
                return value
        
        return value

    def __init__(self, *args, **kwargs):
        processed_kwargs = {}
        annotations = get_type_hints(self)
        
        for name, value in kwargs.items():
            field_type = annotations.get(name)
            if field_type:
                processed_kwargs[name] = _process_value(value, field_type)
            else:
                processed_kwargs[name] = value
        
        original_init(self, **processed_kwargs)
    
    cls.__init__ = __init__
    return cls
