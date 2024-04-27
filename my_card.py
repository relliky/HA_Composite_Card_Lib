#!/usr/bin/env python3

from src.main import HA_Composite_Card_Lib 

hccl = HA_Composite_Card_Lib()
cards = []
# Put your card parameter here
# There are a few examples below
cards += [hccl.getEntityCard(entity='media_player.tv', card_name='电视')]
cards += [hccl.getEntityCard(entity='light.kitchen_ceiling_light', card_name='厨房吸顶灯')]
cards += [hccl.getEntityCard(entity='climate.kitchen', card_name='厨房暖气')]
cards += [hccl.getEntityCard(entity='不需要，这个卡片需要的实体是时辰sensor.shi_chen', card_type='页眉卡片1')]

# Generate your cards in Home Assistant Dashboard yaml format
import os
yaml_path = os.path.dirname(os.path.realpath(__file__)) + '/my_cards.yaml'
hccl.write_to_yaml_config(cards, yaml_path)


