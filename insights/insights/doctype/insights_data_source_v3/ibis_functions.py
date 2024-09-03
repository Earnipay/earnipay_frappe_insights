import frappe
import ibis
from ibis import _
from ibis.expr.types import Column, NumericColumn, StringColumn, TimestampColumn, Value

# generic functions
f_count = Column.count
f_min = Column.min
f_max = Column.max
f_group_concat = Column.group_concat
f_is_in = Value.isin
f_is_not_in = Value.notin
f_is_set = Value.notnull
f_is_not_set = Value.isnull
f_is_between = Value.between
f_coalesce = Value.coalesce
f_distinct_count = Column.nunique
f_sum_if = lambda condition, column: f_sum(column, where=condition)
f_count_if = lambda condition, column: f_count(column, where=condition)
f_if = (
    lambda condition, true_value, false_value: ibis.case()
    .when(condition, true_value)
    .else_(false_value)
    .end()
)
f_sql = lambda query: _.sql(query)


# number Functions
f_abs = NumericColumn.abs
f_sum = NumericColumn.sum
f_avg = NumericColumn.mean
f_round = NumericColumn.round
f_floor = NumericColumn.floor
f_ceil = NumericColumn.ceil

# String Functions
f_lower = StringColumn.lower
f_upper = StringColumn.upper
f_concat = StringColumn.concat
f_replace = StringColumn.replace
f_substring = StringColumn.substr
f_contains = StringColumn.contains
f_not_contains = lambda args, kwargs: ~f_contains(args, kwargs)
f_starts_with = StringColumn.startswith
f_ends_with = StringColumn.endswith


# date functions
f_year = TimestampColumn.year
f_quarter = TimestampColumn.quarter
f_month = TimestampColumn.month
f_week_of_year = TimestampColumn.week_of_year
f_day_of_year = TimestampColumn.day_of_year
f_day_of_week = TimestampColumn.day_of_week
f_day = TimestampColumn.day
f_hour = TimestampColumn.hour
f_minute = TimestampColumn.minute
f_second = TimestampColumn.second
f_microsecond = TimestampColumn.microsecond
f_now = ibis.now
f_today = ibis.today
f_format_date = TimestampColumn.strftime
f_date_diff = TimestampColumn.delta
f_start_of = lambda unit, date: None  # TODO
f_is_within = lambda args, kwargs: None  # TODO

# utility functions
f_to_inr = lambda curr, amount, rate=83: f_if(curr == "USD", amount * rate, amount)
f_to_usd = lambda curr, amount, rate=83: f_if(curr == "INR", amount / rate, amount)
f_literal = ibis.literal
f_row_number = ibis.row_number


def get_functions():
    context = frappe._dict()

    functions = globals()
    for key in functions:
        if key.startswith("f_"):
            context[key[2:]] = functions[key]

    return context


@frappe.whitelist()
def get_function_list():
    return [key[2:] for key in globals() if key.startswith("f_")]