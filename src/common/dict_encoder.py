from typing import List
from enum import Enum


class ObjectNotSerializable(Exception):
    """ Exception for an object is not serializable """
    def __init__(self, message):
        self.message = message


class DictEncoder:
    """ Encodes a any object into a dictionary """
    
    @staticmethod
    def encode(obj: any) -> dict:
        """
        Encodes a any object into a dictionary.
        
        Parameters
        ----------
        obj : any
            The object to encode.
            
        Returns
        -------
        dict
            The encoded dictionary.
        """
        obj_dict = obj
        
        # If the object is a list
        if isinstance(obj, list):
            return DictEncoder._encode_list(obj)
        # If the object has __dict__ set this as initial obj
        if hasattr(obj, '__dict__'):
            obj_dict = { k: v for k, v in obj.__dict__.items() if v is not None }
            
        # If is not list or dict and do not have __dict__ the method cant encode
        if not isinstance(obj_dict, dict):
            raise ObjectNotSerializable(f'Object {obj} is not dict serializable')
        
        # When we have dict
        for key, value in obj_dict.items():
            # If the attribute is list we need to check inside
            if isinstance(value, list):
                obj_dict[key] = DictEncoder._encode_list(value)
            # If the attribute is an enum
            elif isinstance(value, Enum):
                obj_dict[key] = value.value
            # If the attribute has __dict__
            elif hasattr(value, '__dict__'):
                obj_dict[key] = DictEncoder.encode(value)
                        
        return obj_dict    
    
    @staticmethod
    def _encode_list(obj_list: List[any]) -> List[dict]:
        """
        Encodes a list into a list of dictionaries.
        
        Parameters
        ----------
        obj_list : List[any]
            The list to encode.
            
        Returns
        -------
        List[dict]
            The encoded list.
        """
        is_nativy_list = True
        for elem in obj_list:
            if not isinstance(elem, float) and not isinstance(elem, int) and not isinstance(elem, str):
                is_nativy_list = False
                break
        
        if is_nativy_list:
            return obj_list
        
        for index, elem in enumerate(obj_list):
            obj_list[index] = DictEncoder.encode(elem)
        return obj_list