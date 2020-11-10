#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click

from exceptions import TimeoutConnectionError, ConnectError, ValidationError
from utils import get_begin_date, get_end_date
from structure import Params, ResultData
from calculations import get_result_data
from validation import get_valid_params


@get_valid_params
def get_params(**params) -> Params:
    """
    Формирует структуру для хранения параметров скрипта
    :param params:
    :return:
    """
    return Params(
        url=params["url"],
        api_key=params["api_key"],
        begin_date=get_begin_date(params["begin_date"]) if params["begin_date"] else None,
        end_date=get_end_date(params["end_date"]) if params["end_date"] else None,
        branch=params["branch"],
        dev_activity=params["dev_activity"],
        pull_requests=params["pull_requests"],
        issues=params["issues"]
    )


def output_data(result_data: ResultData):
    """
    Вывод результатов работы скрипта.
    :param result_data:
    :return:
    """
    print(f"COMMIT STATISTIC = {result_data.dev_activity}")
    print(f"Number of open pull requests = {result_data.pull_requests.open_pull_requests}")
    print(f"Number of closed pull requests = {result_data.pull_requests.closed_pull_requests}")
    print(f"Number of old pull requests = {result_data.pull_requests.old_pull_requests}")
    print(f"Number of open issues = {result_data.issues.open_issues}")
    print(f"Number of closed issues = {result_data.issues.closed_issues}")
    print(f"Number of old pull issues = {result_data.issues.old_issues}")


@click.command()
@click.argument('url', type=str)
@click.argument('api_key', type=str)
@click.option(
    '--begin_date', '-b', type=str, default="",
    help='analysis start date in format "dd.mm.YYYY"'
)
@click.option(
    '--end_date', '-e', type=str, default="",
    help='analysis end date in format "dd.mm.YYYY"'
)
@click.option(
    '--branch', '-br', type=str, default="master",
    help='repository branch name'
)
@click.option(
    '--dev_activity', '-da', is_flag=True,
    help='analyze developer activity'
)
@click.option(
    '--pull_requests', '-pr', is_flag=True,
    help='analysis of the pull requests on a given branch of the repository'
)
@click.option(
    '--issues', '-i', is_flag=True,
    help='analysis of issues on a given branch of the repository'
)
def main(url, api_key, begin_date, end_date, branch, dev_activity, pull_requests, issues):
    """
    Script for analyzing repository statistics according to the specified parameters.
    If the start and end dates of the analysis are not specified,
    then an unlimited interval is taken to the left, right or completely.
    If the repository branch is not specified, the master branch is taken by default.
    The following events are optionally analyzed:

        1. The activity of developers by the number of commits (--dev_activity).

        2. Statistics of merge requests (--pull_requests).

        3. Issues statistics (--issues).

    If none of the options is specified, then the analysis will be carried out in all directions.
    """
    try:
        params = get_params(
                url=url,
                api_key=api_key,
                begin_date=begin_date,
                end_date=end_date,
                branch=branch,
                dev_activity=dev_activity if True in (dev_activity, pull_requests, issues) else True,
                pull_requests=pull_requests if True in (dev_activity, pull_requests, issues) else True,
                issues=issues if True in (dev_activity, pull_requests, issues) else True
            )
    except ValidationError as err:
        print("Проверьте правильность указания параметров скрипта:\n", "\n".join(err.message))
    except (TimeoutConnectionError, ConnectError) as err:
        print("Проверьте подключение к сети:\n", err)
    else:
        output_data(get_result_data(params))


if __name__ == "__main__":
    main()
