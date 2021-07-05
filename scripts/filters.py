from collections import deque


def make_daily_filter():
    prev_value = 0

    def daily_filter(value):
        nonlocal prev_value
        # Filters out transitions to and from 0 and negative transitions.
        if value and prev_value and value >= prev_value:
            filtered_value = value - prev_value
        else:
            filtered_value = 0
        prev_value = value
        return filtered_value

    return daily_filter


def make_gap_fill_filter():
    prev_value = 0

    def gap_fill_filter(value):
        nonlocal prev_value
        # Fills zeros with previous non-zero value.
        if value:
            filtered_value = value
            prev_value = value
        else:
            filtered_value = prev_value
        return filtered_value

    return gap_fill_filter


def make_rolling_average_filter(window_size):
    rolling_samples = deque()
    rolling_sum = 0

    def rolling_average_filter(sample):
        nonlocal rolling_samples
        nonlocal rolling_sum
        rolling_samples.appendleft(sample)
        rolling_sum += sample
        if len(rolling_samples) > window_size:
            rolling_sum -= rolling_samples.pop()
        # TODO: Should this return a float rather than round to an integer?
        return round(rolling_sum / len(rolling_samples))

    return rolling_average_filter


def run_daily_filter(source):
    daily_result = {}
    daily_filter = make_daily_filter()
    for source_key in sorted(source.keys()):
        daily_result[source_key] = daily_filter(source[source_key])
    return daily_result


def run_gap_fill_filter(source):

    # Fill non-zero forward
    forward_fill_result = {}
    gap_filter = make_gap_fill_filter()
    for source_key in sorted(source.keys()):
        forward_fill_result[source_key] = gap_filter(source[source_key])

    # Fill non-zero backward
    fill_result = {}
    gap_filter = make_gap_fill_filter()
    for fill_key in reversed(sorted(forward_fill_result.keys())):
        fill_result[fill_key] = gap_filter(forward_fill_result[fill_key])

    return fill_result


def run_rolling_average_filter(source, window_size):
    rolling_average = {}
    rolling_average_filter = make_rolling_average_filter(window_size)
    for source_key in sorted(source.keys()):
        rolling_average[source_key] = rolling_average_filter(
            source[source_key])
    return rolling_average
