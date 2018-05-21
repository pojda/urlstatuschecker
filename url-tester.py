import argparse
import URLStatus as us

parser = argparse.ArgumentParser("simple_example")
parser.add_argument("-a", "--all",
                    help="(default) will validate on all user agent platforms (desktop, mobile and tablet)",
                    action="store_true",
                    default=True)

parser.add_argument("-d", "--desktop",
                    help="Validates using Desktop user agent",
                    action="store_true",
                    default=False)

parser.add_argument("-m", "--mobile",
                    help="Validates using Mobile user agent",
                    action="store_true",
                    default=False)

parser.add_argument("-t", "--tablet",
                    help="Validates using Tablet user agent",
                    action="store_true",
                    default=False)

group = parser.add_mutually_exclusive_group()
group.add_argument("--urls-file",
                    help="If specified, will read urls validation from file",
                    default=False)
group.add_argument("--url",
                    help="The URL to be tested",
                    default=False)

parser.add_argument("--user-agents-file",
                    help="If specified, will read User Agents from file (implies -a)",
                    default=False)

args = parser.parse_args()
tester = us.URLStatus(args)