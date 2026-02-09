import datetime

from webtracker import database as db
from pathlib import Path

from webtracker.config import PROJECT_ROOT


def timed_operation(func, *args, operation_name=None, **kwargs):
    # Measures the time to complete an excecuted function and saves the result in the db.
    start_time = datetime.datetime.now()
    result = func(*args, **kwargs)
    end_time = datetime.datetime.now()

    if operation_name is None:
        operation_name = getattr(func, "__name__", "unknown")

    # Save record for performance in db
    try:
        db.save_performance_record(operation_name, start_time, end_time)
    except Exception as err:
        print(f"Error when saving to Performance table: {err}")

    duration = (end_time - start_time).total_seconds()
    return result


def create_performance_report(report_name="Performance report", horizon="today"):
    # Creating perfomance report and refreshing the daily one every time this runs.
    date_time = datetime.datetime.now()

    lines = []
    lines.append("=" * 100)
    lines.append(report_name)
    lines.append(f"Generated: {str(date_time)}.")
    lines.append(f"Horizon: {horizon}.")
    lines.append("=" * 100)
    lines.append("\n")

    if horizon == "today":
        horizon = datetime.datetime.now().date()
    else:
        horizon = ""

    row = db.fetch_performance_records(horizon=horizon)
    recordcount = 0
    operationtime = []
    operationtypes = []

    operations = []

    time_per_operation = 0

    for row in row:
        try:
            recordcount += 1
            operationid = row.get("id")
            operationtime.append(row.get("operation_time"))
            operationtypes.append(row.get("operation"))
            uniqueoperationtypes = set(operationtypes)

            operations.append(
                {
                    "id": operationid,
                    "recordnumber": recordcount,
                    "operation": row.get("operation"),
                    "time": row.get("operation_time"),
                }
            )

        except Exception as err:
            print(err)
            break

    averagetime = sum(operationtime) / recordcount

    lines.append(f"Operation record count: {recordcount}.")
    lines.append(f"Average operation time: {averagetime:.2f} s.")
    lines.append("\n")
    lines.append(f"Operation types:\n {uniqueoperationtypes}.")
    lines.append(f"\n")

    lines.append(f"Performance per operation:")

    for i in uniqueoperationtypes:
        try:
            lines.append(i)
            times = [op["time"] for op in operations if op["operation"] == i]
            time_per_operation = sum(times)
            count_per_operation = len(times)
            if count_per_operation > 0:
                average_per_operation = time_per_operation / count_per_operation
            else:
                average_per_operation = 0.0
            max_per_operation = max(times)
            min_per_operation = min(times)

            lines.append(f"     Count: {count_per_operation}.")
            lines.append(f"     Total time spent: {time_per_operation:.2f} s")
            lines.append(f"     Average time: {average_per_operation:.2f} s.")
            lines.append(f"     Max time: {max_per_operation:.2f} s.")
            lines.append(f"     Min time: {min_per_operation:.2f} s.")
            lines.append(f"\n")

        except Exception as err:
            print(err)
            break

    return "\n".join(lines)


def save_report_to_file(reportcontent=None, filename=None):
    reports_dir = PROJECT_ROOT / "reports" / "performance"
    reports_dir.mkdir(parents=True, exist_ok=True)

    date = datetime.datetime.now().strftime("%Y%m%d")
    filename = filename + date + ".txt"

    filepath = reports_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(reportcontent)


def performance_report_job():
    content = create_performance_report(
        report_name="Daily Performance Report", horizon="today"
    )
    save_report_to_file(content, filename="DailyPerformanceReport")


if __name__ == "__main__":
    timed_operation(performance_report_job)
