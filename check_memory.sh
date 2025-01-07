#!/usr/bin/env bash

ps -eo size,pid,user,command --sort -size > memory-usage-$(date "+%Y%m%d-%H%M%S").log

