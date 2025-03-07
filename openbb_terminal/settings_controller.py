"""Settings Controller Module"""
__docformat__ = "numpy"

# IMPORTATION STANDARD
import argparse
import logging
import os
import os.path
from pathlib import Path
from typing import List, Optional

# IMPORTATION THIRDPARTY
import pytz

from openbb_terminal.config_terminal import i18n_dict_location

# IMPORTATION INTERNAL
from openbb_terminal.core.config.paths import (
    SETTINGS_ENV_FILE,
    USER_DATA_SOURCES_DEFAULT_FILE,
)
from openbb_terminal.core.session.current_user import get_current_user
from openbb_terminal.core.session.preferences_handler import set_preference
from openbb_terminal.custom_prompt_toolkit import NestedCompleter
from openbb_terminal.decorators import log_start_end
from openbb_terminal.helper_funcs import (
    check_positive,
    get_flair,
    get_user_timezone_or_invalid,
    parse_and_split_input,
)
from openbb_terminal.menu import session
from openbb_terminal.parent_classes import BaseController
from openbb_terminal.rich_config import MenuText, console

# pylint: disable=too-many-lines,no-member,too-many-public-methods,C0302
# pylint: disable=import-outside-toplevel

logger = logging.getLogger(__name__)


class SettingsController(BaseController):
    """Settings Controller class"""

    CHOICES_COMMANDS: List[str] = [
        "dt",
        "autoscaling",
        "dpi",
        "backend",
        "height",
        "width",
        "pheight",
        "pwidth",
        "monitor",
        "lang",
        "tz",
        "userdata",
        "source",
        "flair",
        "colors",
        "tbnews",
        "tweetnews",
    ]
    PATH = "/settings/"
    CHOICES_GENERATION = True

    languages_available = [
        lang.strip(".yml")
        for lang in os.listdir(i18n_dict_location)
        if lang.endswith(".yml")
    ]

    def __init__(
        self, queue: Optional[List[str]] = None, env_file: str = str(SETTINGS_ENV_FILE)
    ):
        """Constructor"""
        super().__init__(queue)
        self.env_file = env_file

        if session and get_current_user().preferences.USE_PROMPT_TOOLKIT:
            choices: dict = self.choices_default
            choices["tz"] = {c: None for c in pytz.all_timezones}
            choices["lang"] = {c: None for c in self.languages_available}
            self.choices = choices
            self.completer = NestedCompleter.from_nested_dict(choices)

        self.sort_filter = r"((tz\ -t |tz ).*?("
        for tz in pytz.all_timezones:
            tz = tz.replace("/", r"\/")
            self.sort_filter += f"{tz}|"
        self.sort_filter += ")*)"

    def parse_input(self, an_input: str) -> List:
        """Parse controller input

        Overrides the parent class function to handle github org/repo path convention.
        See `BaseController.parse_input()` for details.
        """
        # Filtering out
        sort_filter = self.sort_filter

        custom_filters = [sort_filter]

        commands = parse_and_split_input(
            an_input=an_input, custom_filters=custom_filters
        )
        return commands

    def print_help(self):
        """Print help"""
        current_user = get_current_user()

        mt = MenuText("settings/")
        mt.add_info("_info_")
        mt.add_raw("\n")
        mt.add_cmd("colors")
        mt.add_setting("dt", current_user.preferences.USE_DATETIME)
        mt.add_cmd("flair")
        mt.add_raw("\n")
        mt.add_param("_flair", get_flair())
        mt.add_raw("\n")
        mt.add_cmd("lang")
        mt.add_raw("\n")
        mt.add_param("_language", current_user.preferences.USE_LANGUAGE)
        mt.add_raw("\n")
        mt.add_cmd("userdata")
        mt.add_raw("\n")
        mt.add_param(
            "_user_data_folder",
            current_user.preferences.USER_DATA_DIRECTORY,
        )
        mt.add_raw("\n")
        mt.add_cmd("tz")
        mt.add_raw("\n")
        mt.add_param("_timezone", get_user_timezone_or_invalid())
        mt.add_raw("\n")
        mt.add_setting("autoscaling", current_user.preferences.USE_PLOT_AUTOSCALING)
        if current_user.preferences.USE_PLOT_AUTOSCALING:
            mt.add_cmd("pheight")
            mt.add_cmd("pwidth")
            mt.add_raw("\n")
            mt.add_param(
                "_plot_height_pct",
                current_user.preferences.PLOT_HEIGHT_PERCENTAGE,
                16,
            )
            mt.add_param(
                "_plot_width_pct",
                current_user.preferences.PLOT_WIDTH_PERCENTAGE,
                16,
            )
        else:
            mt.add_cmd("height")
            mt.add_cmd("width")
            mt.add_raw("\n")
            mt.add_param("_plot_height", current_user.preferences.PLOT_HEIGHT, 12)
            mt.add_param("_plot_width", current_user.preferences.PLOT_WIDTH, 12)
        mt.add_raw("\n")
        mt.add_cmd("dpi")
        mt.add_raw("\n")
        mt.add_param("_dpi", current_user.preferences.PLOT_DPI)
        mt.add_raw("\n")
        mt.add_cmd("backend")
        mt.add_raw("\n")
        mt.add_param("_backend", current_user.preferences.PLOT_BACKEND)
        mt.add_raw("\n")
        mt.add_cmd("monitor")
        mt.add_raw("\n")
        mt.add_param("_monitor", current_user.preferences.MONITOR)
        mt.add_raw("\n")
        mt.add_cmd("source")
        mt.add_raw("\n")
        mt.add_param(
            "_data_source", current_user.preferences.PREFERRED_DATA_SOURCE_FILE
        )
        mt.add_raw("\n")
        mt.add_setting("tbnews", current_user.preferences.TOOLBAR_TWEET_NEWS)
        if current_user.preferences.TOOLBAR_TWEET_NEWS:
            mt.add_raw("\n")
            mt.add_cmd("tweetnews")
            mt.add_raw("\n")
            mt.add_param(
                "_tbnu",
                current_user.preferences.TOOLBAR_TWEET_NEWS_SECONDS_BETWEEN_UPDATES,
            )
            mt.add_param(
                "_nttli",
                current_user.preferences.TOOLBAR_TWEET_NEWS_NUM_LAST_TWEETS_TO_READ,
            )
            mt.add_param(
                "_tatt", current_user.preferences.TOOLBAR_TWEET_NEWS_ACCOUNTS_TO_TRACK
            )
            mt.add_param("_tk", current_user.preferences.TOOLBAR_TWEET_NEWS_KEYWORDS)
        console.print(text=mt.menu_text, menu="Settings")

    @log_start_end(log=logger)
    def call_colors(self, other_args: List[str]):
        """Process colors command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="autoscaling",
            description="Set the use of autoscaling in the plots",
        )
        ns_parser = self.parse_simple_args(parser, other_args)
        if ns_parser:
            console.print(
                "\n1. Play with the terminal coloring embedded in our website https://openbb.co/customize\n"
            )
            console.print("2. Once happy, click 'Download Theme'\n")
            console.print(
                "3. The file 'openbb_config.richstyle.json' should be downloaded\n"
            )
            console.print(
                "4. Insert that config file inside /OpenBBUserData/styles/user/\n"
            )
            console.print("5. Close the terminal and run it again.\n")

    @log_start_end(log=logger)
    def call_dt(self, other_args: List[str]):
        """Process dt command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="dt",
            description="Set the use of datetime in the plots",
        )
        ns_parser = self.parse_simple_args(parser, other_args)
        if ns_parser:
            set_preference(
                "USE_DATETIME", not get_current_user().preferences.USE_DATETIME
            )

    @log_start_end(log=logger)
    def call_source(self, other_args: List[str]):
        """Process source command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="source",
            description="Preferred data source file.",
        )
        parser.add_argument(
            "-f",
            "--file",
            type=str,
            default=str(USER_DATA_SOURCES_DEFAULT_FILE),
            dest="file",
            help="file",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-f")
        ns_parser = self.parse_simple_args(parser, other_args)
        if ns_parser:
            if os.path.exists(ns_parser.file):
                set_preference("PREFERRED_DATA_SOURCE_FILE", ns_parser.file)
                console.print("[green]Sources file changed successfully![/green]")
            else:
                console.print("[red]Couldn't find the sources file![/red]")

    @log_start_end(log=logger)
    def call_autoscaling(self, other_args: List[str]):
        """Process autoscaling command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="autoscaling",
            description="Set the use of autoscaling in the plots",
        )
        ns_parser = self.parse_simple_args(parser, other_args)
        if ns_parser:
            set_preference(
                "USE_PLOT_AUTOSCALING",
                not get_current_user().preferences.USE_PLOT_AUTOSCALING,
            )

    @log_start_end(log=logger)
    def call_dpi(self, other_args: List[str]):
        """Process dpi command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="dpi",
            description="Dots per inch.",
        )
        parser.add_argument(
            "-v",
            "--value",
            type=int,
            dest="value",
            help="value",
            required="-h" not in other_args,
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-v")
        ns_parser = self.parse_simple_args(parser, other_args)
        if ns_parser and ns_parser.value:
            set_preference("PLOT_DPI", ns_parser.value)

    @log_start_end(log=logger)
    def call_height(self, other_args: List[str]):
        """Process height command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="height",
            description="select plot height (autoscaling disabled)",
        )
        parser.add_argument(
            "-v",
            "--value",
            type=int,
            dest="value",
            help="value",
            required="-h" not in other_args,
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-v")
        ns_parser = self.parse_simple_args(parser, other_args)
        if ns_parser:
            set_preference("PLOT_HEIGHT", ns_parser.value)

    @log_start_end(log=logger)
    def call_width(self, other_args: List[str]):
        """Process width command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="width",
            description="select plot width (autoscaling disabled)",
        )
        parser.add_argument(
            "-v",
            "--value",
            type=int,
            dest="value",
            help="value",
            required="-h" not in other_args,
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-v")
        ns_parser = self.parse_simple_args(parser, other_args)
        if ns_parser:
            set_preference("PLOT_WIDTH", ns_parser.value)

    @log_start_end(log=logger)
    def call_pheight(self, other_args: List[str]):
        """Process pheight command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="pheight",
            description="select plot height percentage (autoscaling enabled)",
        )
        parser.add_argument(
            "-v",
            "--value",
            type=float,
            dest="value",
            help="value",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-v")
        ns_parser = self.parse_simple_args(parser, other_args)
        if ns_parser:
            set_preference("PLOT_HEIGHT_PERCENTAGE", ns_parser.value)

    @log_start_end(log=logger)
    def call_pwidth(self, other_args: List[str]):
        """Process pwidth command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="pwidth",
            description="select plot width percentage (autoscaling enabled)",
        )
        parser.add_argument(
            "-v",
            "--value",
            type=float,
            dest="value",
            help="value",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-v")
        ns_parser = self.parse_simple_args(parser, other_args)
        if ns_parser:
            set_preference("PLOT_WIDTH_PERCENTAGE", ns_parser.value)

    @log_start_end(log=logger)
    def call_monitor(self, other_args: List[str]):
        """Process pwidth command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="pwidth",
            description="choose which monitor to scale: 0-primary, 1-secondary (autoscaling enabled)",
        )
        parser.add_argument(
            "-v",
            "--value",
            type=int,
            dest="value",
            help="value",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-v")
        ns_parser = self.parse_simple_args(parser, other_args)
        if ns_parser:
            set_preference("MONITOR", ns_parser.value)

    @log_start_end(log=logger)
    def call_backend(self, other_args: List[str]):
        """Process backend command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="backend",
            description="Backend to use for plotting",
        )
        parser.add_argument(
            "-v",
            "--value",
            type=str,
            dest="value",
            help="value",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-v")
        ns_parser = self.parse_simple_args(parser, other_args)
        if ns_parser:
            set_preference("BACKEND", ns_parser.value)

    @log_start_end(log=logger)
    def call_lang(self, other_args: List[str]):
        """Process lang command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="lang",
            description="Choose language for terminal",
        )
        parser.add_argument(
            "-v",
            "--value",
            type=str,
            dest="value",
            help="Language",
            choices=self.languages_available,
            default="",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-v")
        ns_parser = self.parse_simple_args(parser, other_args)
        if ns_parser:
            if ns_parser.value:
                set_preference("USE_LANGUAGE", ns_parser.value)
            else:
                console.print(
                    f"Languages available: {', '.join(self.languages_available)}"
                )

    @log_start_end(log=logger)
    def call_tz(self, other_args: List[str]):
        """Process tz command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description="""
                   Setting a different timezone
               """,
        )
        parser.add_argument(
            "-t",
            dest="timezone",
            help="Choose timezone",
            required="-h" not in other_args,
            metavar="TIMEZONE",
            choices=pytz.all_timezones,
        )

        if other_args and "-t" not in other_args[0]:
            other_args.insert(0, "-t")

        ns_parser = self.parse_simple_args(parser, other_args)
        if ns_parser and ns_parser.timezone:
            set_preference("TIMEZONE", ns_parser.timezone)

    @log_start_end(log=logger)
    def call_flair(self, other_args: List[str]):
        """Process flair command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="flair",
            description="set the flair emoji to be used",
        )
        parser.add_argument(
            "-e",
            "--emoji",
            type=str,
            dest="emoji",
            help="flair emoji to be used",
            nargs="+",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-e")
        ns_parser = self.parse_simple_args(parser, other_args)
        if ns_parser:
            if not ns_parser.emoji:
                ns_parser.emoji = ""
            else:
                ns_parser.emoji = " ".join(ns_parser.emoji)

            set_preference("FLAIR", ns_parser.emoji)

    @log_start_end(log=logger)
    def call_userdata(self, other_args: List[str]):
        """Process userdata command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="userdata",
            description="Set folder to store user data such as exports, presets, logs",
        )
        parser.add_argument(
            "--folder",
            type=str,
            dest="folder",
            help="Folder where to store user data. ",
            default=f"{str(Path.home() / 'OpenBBUserData')}",
        )
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "--folder")
        ns_parser = self.parse_simple_args(parser, other_args)

        if ns_parser and (other_args or self.queue):
            userdata_path = "" if other_args else "/"

            userdata_path += "/".join([ns_parser.folder] + self.queue)
            self.queue = []

            userdata_path = userdata_path.replace("'", "").replace('"', "")

            default_path = Path.home() / "OpenBBUserData"

            success_userdata = False
            while not success_userdata:
                if userdata_path.upper() == "DEFAULT":
                    console.print(
                        f"User data to be saved in the default folder: '{default_path}'"
                    )
                    set_preference("USER_DATA_DIRECTORY", default_path)
                    success_userdata = True
                else:
                    # If the path selected does not start from the user root, give relative location from root
                    if userdata_path[0] == "~":
                        userdata_path = userdata_path.replace(
                            "~", os.path.expanduser("~")
                        )

                    # Check if the directory exists
                    if os.path.isdir(userdata_path):
                        console.print(
                            f"User data to be saved in the selected folder: '{userdata_path}'"
                        )
                        set_preference("USER_DATA_DIRECTORY", userdata_path)
                        success_userdata = True
                    else:
                        console.print(
                            "[red]The path selected to user data does not exist![/red]\n"
                        )
                        user_opt = "None"
                        while user_opt not in ("Y", "N"):
                            user_opt = input(
                                f"Do you wish to create folder: `{userdata_path}` ? [Y/N]\n"
                            ).upper()

                        if user_opt == "Y":
                            os.makedirs(userdata_path)
                            console.print(
                                f"[green]Folder '{userdata_path}' successfully created.[/green]"
                            )
                            set_preference("USER_DATA_DIRECTORY", userdata_path)
                        else:
                            # Do not update userdata_folder path since we will keep the same as before
                            console.print(
                                "[yellow]User data to keep being saved in "
                                + "the selected folder: "
                                + f"{str(get_current_user().preferences.USER_DATA_DIRECTORY)}[/yellow]"
                            )
                        success_userdata = True

        console.print()

    @log_start_end(log=logger)
    def call_tbnews(self, other_args):
        """Process tbnews command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="tweetnews",
            description="Tweak tweet news toolbal parameters",
        )
        ns_parser = self.parse_known_args_and_warn(parser, other_args)
        if ns_parser:
            current_user = get_current_user()
            if current_user.preferences.TOOLBAR_TWEET_NEWS:
                console.print("Will take effect when running terminal next.")
            set_preference(
                "TOOLBAR_TWEET_NEWS",
                not get_current_user().preferences.TOOLBAR_TWEET_NEWS,
            )

    @log_start_end(log=logger)
    def call_tweetnews(self, other_args: List[str]):
        """Process tweetnews command"""
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="tweetnews",
            description="Tweak tweet news parameters",
        )
        parser.add_argument(
            "-t",
            "--time",
            type=check_positive,
            required=False,
            dest="time",
            help="Time (in seconds) between tweet news updates, e.g. 300",
        )
        parser.add_argument(
            "-a",
            "--accounts",
            type=str,
            required=False,
            dest="accounts",
            help="Twitter accounts to track news separated by commmas."
            "For instance: 'WatcherGuru,unusual_whales,gurgavin'",
        )
        parser.add_argument(
            "-k",
            "--keywords",
            type=str,
            required=False,
            dest="keywords",
            nargs="+",
            help="Keywords to look for, separated by commmas."
            "For instance: 'Just In, Breaking'",
        )
        parser.add_argument(
            "-n",
            "--number",
            type=check_positive,
            required=False,
            dest="number",
            help="Number of tweets to look into from each account, e.g. 3",
        )
        ns_parser = self.parse_known_args_and_warn(parser, other_args)
        if ns_parser:
            if ns_parser.time:
                set_preference(
                    "TOOLBAR_TWEET_NEWS_SECONDS_BETWEEN_UPDATES",
                    str(ns_parser.time),
                )

            if ns_parser.number:
                set_preference(
                    "TOOLBAR_TWEET_NEWS_NUM_LAST_TWEETS_TO_READ",
                    str(ns_parser.number),
                )

            if ns_parser.accounts:
                set_preference(
                    "TOOLBAR_TWEET_NEWS_ACCOUNTS_TO_TRACK",
                    str(ns_parser.accounts),
                )

            if ns_parser.keywords:
                set_preference(
                    "TOOLBAR_TWEET_NEWS_KEYWORDS",
                    str(" ".join(ns_parser.keywords)),
                )
