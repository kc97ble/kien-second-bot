#!/usr/bin/env python3

def format_stages(stages):
    return "\n".join(map(lambda m : m['item'], stages))

def format_movement_list(m_list):
    return "\n".join(map(lambda m : "%s (%sed on %s)"
        % (m['item'], m['action'], m['date']), m_list))
