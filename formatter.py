#!/usr/bin/env python3

def format_stages(stages):
    return "\n".join(map(lambda m : m['item'], stages))
