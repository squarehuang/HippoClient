#!/usr/bin/env bash

date_cmd=$( which date )
[[ ! -e $date_cmd ]] && date_cmd="/bin/date"

function _tstamp () { _ts=$($date_cmd +'%F %T'); echo "$_ts [$( hostname )]"; }
function _format () { _ts=$(_tstamp);_bn=$(basename $0); echo "$_ts $_sev ($_bn) $*"; }

function log_fatal ()   { _sev="FATAL"; _format $* >&2; }
function log_error ()   { _sev="ERROR"; _format $* >&2; }
function log_warn ()    { _sev="WARN";  _format $* >&2; }
function log_info ()    { _sev="INFO";  _format $* >&2; }
function log_debug ()   { _sev="DEBUG"; _format $* >&2; }
