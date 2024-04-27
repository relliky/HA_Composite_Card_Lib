#!/usr/bin/env python3

import re
import yaml
import os

class HA_Composite_Card_Lib:

  def __init__ (self):
    pass

  # for lovelace single entity:
  # entity
  # entity_name
  # entity_name_translation
  # card name -> can be inferred from entity name -> can be inferred from entity
  # card type -> can be inferred from entity type
  # card icon -> can be inferred from device icon if added
  # card icon color 
  # double tab action
  def getEntityCard(self, entity, entity_name=None, entity_name_translation=None, 
                          card_name=None, card_type=None,card_icon=None,card_icon_color=None,double_tab_action=None,simple=None,
                          secondary_info=None):
    card = {}     
    
    # Set up card_type based on entity_type
    if card_type is None:

      # remove entity name to get entity type
      # "light" = Remove ".living_room_ceiling_light" from "light.living_room_ceiling_light"
      entity_type = re.sub("\.(\w+)$", "", entity)

      if entity_type in ['light', 'cover', 'climate']:
        card_type = 'custom:mushroom-' + entity_type    + '-card'
      elif entity_type in ['media_player']:
        card_type = 'custom:mushroom-' + 'media-player' + '-card'
      if entity_type in ['binary_sensor', 'switch', 'input_boolean']:
        card_type = 'custom:mushroom-' + 'entity'       + '-card'
      elif entity_type in ['group']:
        card_type = 'custom:auto-entities'
      elif entity_type in ['sensor']:
        card_type = 'sensor'
      elif entity_type in ['input_select']:
        card_type = 'custom:mushroom-select-card'
      elif entity_type in ['input_number', 'number']:
        card_type = 'custom:mushroom-number-card'

    if entity_name is None:
      entity_name = self.getName(entity)

    #if card_name is None:
    #  # Remove room name from entity name to get card name
    #  # "Ceiling Light" = Remove "Living Room" from "Living Room Ceiling Light" 
    #  card_name = re.sub(self.room_name, "", entity_name)
    #  #if self.chinese == True:
 

    #if entity_name_translation != None:
    #  entity_name_translation = 

    card_name = '' if card_name is None else card_name
    #if self.dashboard_language is 'Chinese':
    #  card_name = translator.translate(card_name)
    #  print (card_name)     
    card_icon = '' if card_icon is None else card_icon

    # light
    if card_type == 'custom:mushroom-light-card':
      card = {
        "type": card_type,
        "fill_container": True,
        "use_light_color": False,
        "show_brightness_control": True,
        "show_color_control": False,
        "show_color_temp_control": True,
        "collapsible_controls": False,
        "name": card_name,
        "icon": card_icon,
        "entity": entity
      } | self.getCardMod('ios16_toggle', card_type=card_type, color='ios_yellow')
    
    # cover
    elif card_type == 'custom:mushroom-cover-card':
      card = {
        "type": card_type,
        "fill_container": True,
        "tap_action":{
          "action": "toggle"
        },
        "double_tap_action":{
          "action": "more-info"
        },
        "hold_action":{
          "action": "more-info"
        },                
        "show_position_control": True,
        "show_buttons_control": True,
        "name": card_name,
        "icon": card_icon,
        "entity": entity
      }

    # climate
    elif card_type == 'custom:mushroom-climate-card':
      card = {
        "type": card_type,
        "show_temperature_control": True,
        "collapsible_controls": False,
        "name": card_name,
        "icon": card_icon,
        "entity": entity
      }

    # media_player card
    # tap - toggle/navigate/more-info
    elif card_type == 'custom:mushroom-media-player-card':
      card = {
        "type": card_type,
        "fill_container": True,
        "tap_action":{
          "action": "more-info"
        },
        "volume_controls":[
         # "volume_mute",
          "volume_set",
          "volume_buttons"
        ],
        "show_volume_level": False,
        "name": card_name,
        "icon": card_icon,
        "entity": entity
      }
    # group card
    elif card_type == 'custom:auto-entities':
      card = {
        "type": card_type,
        "card":{
          "type": "entities",
          "title": card_name
        },
        "filter": {"include": [{"group": entity}]}
      }

    # sensor
    elif card_type == 'sensor':
      if simple is True:
        card = {
          "type": card_type,
          "graph": "line",
          "name": card_name,
          "icon": card_icon,
          "entity": entity
        }
      else: # complex minigraph temperature sensor card from 
      # https://bbs.hassbian.com/forum.php?mod=redirect&goto=findpost&ptid=22509&pid=550976
        card = {
          "type": "custom:vertical-stack-in-card",
          "cards": [
            {
              "type": "custom:mushroom-template-card",
              "entity": entity,
              "primary": card_name,
              "secondary": "{{ states('" + entity + "') | round(0) }}\u00b0C\n",
              "icon": "mdi:thermometer",
              "icon_color": "{% set value = states('" + entity + "') | int %}\n{% if value < 18 %}\n  blue\n{% elif value < 28 %}\n  light-green\n{% elif value < 40 %}\n  red\n{% else %}\n  green\n{% endif %}",
              "tap_action": {
                "action": "more-info"
              }
            } | self.getCardModColor('transparent'),
            {
              "type": "custom:layout-card",
              "layout_type": "masonry",
              "layout": {
                "width": 150,
                "max_cols": 1,
                "height": "auto",
                "padding": "0px",
                "card_margin": "var(--masonry-view-card-margin, -10px 8px 15px)"
              },
              "cards": [
                {
                  "type": "custom:mini-graph-card",
                  "tap_action": {
                    "action": "more-info"
                  },
                  "entities": [
                    {
                      "entity": entity,
                      "name": "Temperature"
                    }
                  ],
                  "color_thresholds": [
                    {
                      "value": -10,
                      "color": "#0000ff"
                    },
                    {
                      "value": 18,
                      "color": "#0000ff"
                    },
                    {
                      "value": 18.1,
                      "color": "#00FF00"
                    },
                    {
                      "value": 27,
                      "color": "#00FF00"
                    },
                    {
                      "value": 27.1,
                      "color": "#FF0000"
                    },
                    {
                      "value": 40,
                      "color": "#FF0000"
                    }
                  ],
                  "hours_to_show": 24,
                  "line_width": 3,
                  "animate": True,
                  "show": {
                    "name": False,
                    "icon": False,
                    "state": False,
                    "legend": False,
                    "fill": "fade"
                  },
                  "card_mod": {
                    "style": "ha-card {\n  background: none;\n  box-shadow: none;\n  --ha-card-border-width: 0;\n}"
                  }
                }
              ]
            }
          ]
        }

    # entity card
    # binary_sensor    - tap to more-info
    # switch           - tap to toggle
    # input boolean
    elif card_type == 'custom:mushroom-entity-card':
      card = {
        "type": card_type,
        "fill_container": True,
        "tap_action":{
          "action": "toggle"
        },
        "name": card_name,
        "icon": card_icon,
        "entity": entity
      }
    
    # entities card
    # input_timer
    elif card_type == 'entities':
      card = {
        "type": card_type,
        "entities":[
          { "name":   card_name,
            "entity": entity}
        ]
      }

    # schduler card
    elif card_type == 'custom:scheduler-card':
      card = {
        "type": card_type,
        "include": entity,
        "exclude": [],
        "title": True,
        "discover_existing": True,
        "time_step": 30        
      }

    # timer card
    elif card_type == 'custom:flipdown-timer-card':
      card = {
        "type": card_type,
        "show_hour": True,
        "show_title": True,
        "theme": 'dark',
        "styles": {
          "rotor": {
            "width": "50px",
            "height": "80px"},
          "button": {
            "width": "100px",
            "location": "bottom"}
        },
        "name": card_name,
        "icon": card_icon,
        "entity": entity
      }

    # input_number
    # number
    elif card_type == 'custom:mushroom-number-card':
      card = {
        "type": card_type,
        "fill_container": True,
        "tap_action":{
          "action": "more-info"
        },
        "display_mode": "buttons",
        "name": card_name,
        "icon": 'mdi:counter' if card_icon is None else card_icon,
        "entity": entity
      }

    # input_select
    elif card_type == 'custom:mushroom-select-card':
      card = {
        "type": card_type,
        "fill_container": True,
        "tap_action":{
          "action": "more-info"
        },
        "icon": "mdi:brightness-4" if card_icon is None else card_icon,
        "secondary_info": state if secondary_info is None else secondary_info,
        "name": card_name,
        "entity": entity
      }


    # input_select
    elif card_type == '页眉卡片1':
      card = {
        "type": "custom:mod-card",
        "card": {
            "type": "custom:button-card",
            "show_icon": False,
            "show_state": False,
            "show_name": False,
            "styles": {
                "grid": [
                    {"grid-template-areas": '"a a b c"'},
                    {"grid-template-columns": "1fr 3fr 1fr 1fr"},
                    {"grid-template-rows": "1fr"}
                ],
                "card": [{"padding": "8px"}]
            },
            "custom_fields": {
                "a": {
                    "card": {
                        "type": "custom:mushroom-chips-card",
                        "chips": [
                            {"type": "menu"}
                        ]
                    }
                },
                "b": {
                    "card": {
                        "type": "custom:mushroom-chips-card",
                        "chips": [
                            {
                                "type": "template",
                                "entity": "sensor.time",
                                "content": "{{ states(entity) }}",
                                "tap_action": {"action": "more-info"}
                            }
                        ]
                    }
                },
                "c": {
                    "card": {
                        "type": "custom:mushroom-chips-card",
                        "chips": [
                            {
                                "type": "template",
                                "entity": "sensor.shi_chen",
                                "content": "{{ states(entity) }}",
                                "tap_action": {"action": "more-info"}
                            }
                        ]
                    }
                }
            }
        },
        "card_mod": {
            "style": """
                :host {
                    z-index: 5;
                    position: sticky;
                    position: -webkit-sticky;
                    top: 0;
                }
            """
        }
    }
    return card

  def getCardMod(self, style='background_color_select', card_type=None, color=None, support_dark_mode=True):
    css_variable = ""

    if style == 'background_color_select':
      css_variable += ":host { --ha-card-background:" + self.getColor(color) + ";}\n" 

    elif style == 'ios16_toggle':
      entity_is_on_condition = " (states(config.entity) in ['on']) " + \
                                  ("and (states('sun.sun') != 'below_horizon')" if support_dark_mode == True else '')

      # Make card background white if on, dark if off
      css_variable += (":host {\n"
      "--ha-card-background:    {% if" + entity_is_on_condition + "%} " + self.getColor("less_transparent_white") + "  {% else  %} " + self.getColor("more_transparent_grey") + "  {% endif %};\n" 
      "--primary-text-color:    {% if" + entity_is_on_condition + "%} black                                            {% else  %} white                                           {% endif %};\n" 
      "--secondary-text-color : {% if" + entity_is_on_condition + "%} " + self.getColor("dark_grey") +                "{% else  %} " + self.getColor("light_grey") +             " {% endif %};\n"
      ";}\n")
      
      # Make icon a bit larger, similar to ios 16
      css_variable += ("ha-card > mushroom-card > mushroom-state-item > mushroom-shape-icon > ha-state-icon {\n"
      "--mdc-icon-size: 0.6em;"
      ";}\n")

      # Make icon inner white if on, outter dark if off
      if card_type == 'custom:mushroom-light-card':
          css_variable +=  "ha-card > mushroom-card > mushroom-state-item > mushroom-shape-icon {"       + " \n" + \
            "--icon-color-disabled:   " + self.getColor(color)                                           + ";\n" + \
            "--shape-color-disabled:  " + self.getColor("more_transparent_grey")                         + ";\n" + \
            "--icon-color:            " + self.getColor("white")                                         + ";\n" + \
            "--shape-color:            {% if state_attr(config.entity, 'color_mode') == 'color_temp' %}" + " \n" + \
                                          self.getColor(color)                                           + " \n" + \
                                      "{% else  %}"                                                      + " \n" + \
                                      "   rgb{{state_attr(config.entity, 'rgb_color')}}"                 + " \n" + \
                                      "{% endif%}"                                                       + ";\n" + \
            "}\n"

      else:
        css_variable += ( "ha-card > mushroom-card > mushroom-state-item > mushroom-shape-icon {\n"
          "--icon-color-disabled:  " + self.getColor(color)            + ";\n"
          "--shape-color-disabled: " + self.getColor("more_transparent_grey") + ";\n"
          "--icon-color:           " + self.getColor("white")                 + ";\n"
          "--shape-color:          " + self.getColor(color)            + ";\n"
          "}\n")

      # Make light card brightness slider color same as the light color if it is in RGB, otherwise use ios_yellow
      if card_type == 'custom:mushroom-light-card':
          css_variable +=  "ha-card > mushroom-card > div > mushroom-light-brightness-control {"         + " \n" + \
            "--slider-color:           {% if state_attr(config.entity, 'color_mode') == 'color_temp' %}" + " \n" + \
                                          self.getColor(color)                                           + " \n" + \
                                      "{% else  %}"                                                      + " \n" + \
                                      "   rgb{{state_attr(config.entity, 'rgb_color')}}"                 + " \n" + \
                                      "{% endif%}"                                                       + ";\n" + \
            "--slider-bg-color:        {% if state_attr(config.entity, 'color_mode') == 'color_temp' %}" + " \n" + \
                                          "{{ '" + self.getColor(color) + "' | regex_replace(',([\d\.])+\)$', ',0.2)') }}" + " \n" + \
                                      "{% else  %}"                                                      + " \n" + \
                                      "   rgba{{(state_attr(config.entity, 'rgb_color')|string)[0:-1]}}, 0.2)"  + " \n" + \
                                      "{% endif%}"                                                       + ";\n" + \
            "}\n"

      # Make bottom buttons background more visiable in white card
      # and default in dark card
      if card_type == 'custom:mushroom-light-card':
        for index in [2,3]:
          css_variable += "" + \
            "ha-card > mushroom-card > div > mushroom-button:nth-child(" + str(index) + ") {"
          css_variable += "" + \
            "  --bg-color: {% if " + entity_is_on_condition + " %} " + self.getColor("less_transparent_white") + " {% else %} rgba(var(--rgb-primary-text-color), 0.05)" +  " {% endif %};" + \
            "}\n"
        
    else: 
      raise TypeError( "\n" +\
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n" + \
          "getCardMod does not support style = " + style + \
          "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")

    return {
      "card_mod": {
        "style":  css_variable 
      }    
    }

  def getColor(self, color):
    # The last digit of rgba represents opacity and the value of it is between 0.0 and 1.0 
    # !! always needs to follow the rgba format to maintain a compatibility 
    if color == 'transparent':
      return "rgba(245, 245, 245, 0)"
    elif color == 'more_transparent_grey':
      return "rgba(10, 10, 10, 0.4)"
    elif color == 'less_transparent_grey':
      return "rgba(10, 10, 10, 0.7)"
    elif color == 'most_transparent_white':
      return "rgba(245, 245, 245, 0.1)"
    elif color == 'more_transparent_white':
      return "rgba(245, 245, 245, 0.3)"
    elif color == 'less_transparent_white':
      return "rgba(245, 245, 245, 0.9)"
    elif color == 'dark_grey':
      return "rgba(100, 100, 100, 1)"
    elif color == 'light_grey':
      return "rgba(220, 220, 220, 1)"
    elif color == 'ios_yellow':
      return "rgba(253,204,0,1)"
    else: 
      return color

  def getCardModColor(self, color):
    return self.getCardMod('background_color_select', color=color)

  def getTemplateCard(self, icon='mdi:head-alert-outline', 
                            icon_color='blue', 
                            primary=None, 
                            secondary=None, 
                            condition_entity=None, 
                            tap_entity=None, 
                            condition_state='on', 
                            condition_state_not=None, 
                            condition_states=None,
                            tap_action='more-info',
                            theme='default'):
    
    self.dashboard_view_path = "/" + self.dashboard_root + "/" + self.room_navi_path
    
    tap_action_dict = {}
    entity =  tap_entity                  if tap_entity       != None else \
              condition_entity            if condition_entity != None else \
              'input_boolean.placeholder'
             
    if   tap_action == 'navigate':
      tap_action_dict = {
        "action": "navigate",
        "navigation_path": self.dashboard_view_path} 
    elif tap_action == 'more-info':
      tap_action_dict = {"action": "more-info"}
    
    template_card = {
      "type":       "custom:mushroom-template-card",
      "icon":       "{% set entity = '"+entity+"' %}\n" + icon,
      "tap_action": tap_action_dict,
      "entity":     entity,
      "layout":     "horizontal",
      "fill_container": True,
    } | ({"primary"   : primary                                         } if primary   != None      else {}) \
      | ({"secondary" : secondary                                       } if secondary != None      else {}) \
      | ({"icon_color": "{% set entity = '"+entity+"' %}\n" + icon_color} if theme     == 'default' else {}) 

    if condition_entity == None:
      condition_card = template_card
    else:
      condition_card = {}

      # Use single condition
      if condition_states is None:
        condition_card = {
          "type": "conditional",
          "conditions": [
            ( {"entity":    condition_entity}) | ( 
              {"state_not": condition_state_not} if condition_state_not != None else \
              {"state":     condition_state}    )
          ],
          "card": template_card }
          
      else: # Use multiple conditions 
        condition_card = {
          "type": "custom:state-switch",
          "entity": condition_entity,
          states: {}}
        for state in condition_states:
          condition_card['states'] |= { state : template_card}

    if theme == 'ios':
      #condition_card |= self.getCardMod(style='ios16_toggle',color=("{% set entity = '"+entity+"' %}\n" + icon_color))
      condition_card |= self.getCardMod(color=("{% set entity = '"+entity+"' %}\n" + icon_color))

    return condition_card

  def getPostfix(self, entity):
    postfix = re.sub("^.*\.", "", entity)
    
    # This regex does not seem to work to capture special characters
    if re.search('[\./!"£$%^&*()]', postfix) != None:
      raise TypeError( "\n" +\
                       "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n" + \
                       "Postfix " + postfix + " still have specical characters $./!\"£$%^&*()" + "\n" + \
                       "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
    return postfix

  def convertPostfixToName(self, postfix):
    return re.sub("_", " ", postfix)

  # match the beginning of the string or a space, followed by a non-space
  def captilizeSentence(self, s):
    return re.sub("(^|\s)(\S)", lambda m: m.group(1) + m.group(2).upper(), s)

  def getName(self, entity):
    postfix = self.getPostfix(entity)
    name    = self.convertPostfixToName(postfix)
    name    = self.captilizeSentence(name)
    return  name

  # Create a new yaml and write to it
  def write_to_yaml_config (self, my_card_list, yaml_path):
      yaml.Dumper.ignore_aliases = lambda *args : True
      # Open a new file and write automation
      f = open(yaml_path, "w")
      f.write("#############################################################################\n")
      f.write("# DO NOT MODIFY. This is an automatically generated file.                   # \n")      
      f.write("#############################################################################\n")  
      f.write(yaml.dump(my_card_list, sort_keys=False, width=float("inf")))
      f.close()

