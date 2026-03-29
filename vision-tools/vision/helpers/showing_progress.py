def showing_progress(collection, *args, **kwargs):
    if hasattr(collection, "__len__") or "total" in kwargs:
        for i in showing_progress_total(collection, *args, **kwargs):
            yield i
    else:
        for i in showing_progress_nototal(collection, *args, **kwargs):
            yield i


def showing_progress_total(collection, total=None, step=1, bar_length=100, message="Progress: {bar} {percent:.0f}% ({counter}/{total})"):
    if total is None:
        if hasattr(collection, "__len__"):
            total = len(collection)

    if total is None:
        raise Exception("Cannot determine length of the collection")

    last_percent = -999.
    bar = ""
    if bar_length:
        step = min(step, 100./bar_length)

    counter = -1
    for counter, item in enumerate(collection):
        percent = 100.0 * counter / total
        if percent >= last_percent + step:
            if bar_length:
                bl = min(int(round(percent/100*bar_length)), bar_length)
                bar = "|" + "#" * bl + " " * (bar_length-bl) + "|"
            print(message.format(percent=percent, counter=counter, total=total, bar=bar))
            last_percent = percent
        yield item

    if bar_length:
        bar = "|" + "#" * bar_length + "|"
    print(message.format(percent=100, counter=total, total=total, bar=bar))


def showing_progress_nototal(collection, message="Progress: {counter}"):
    counter = -1
    next_show = 0
    for counter, item in enumerate(collection):
        if counter >= next_show:
            print(message.format(counter=counter))
            next_show = counter * 1.2
        yield item

    counter += 1
    print(message.format(counter=counter))
