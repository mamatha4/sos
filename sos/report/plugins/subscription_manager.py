# This file is part of the sos project: https://github.com/sosreport/sos
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

from sos.report.plugins import Plugin, RedHatPlugin
import glob


class SubscriptionManager(Plugin, RedHatPlugin):

    short_desc = 'subscription-manager information'

    plugin_name = 'subscription_manager'
    profiles = ('system', 'packagemanager', 'sysmgmt')

    files = ('/etc/rhsm/rhsm.conf',)
    packages = ('subscription-manager',)

    def setup(self):
        # rhsm config and logs
        self.add_copy_spec([
            "/etc/rhsm/",
            "/var/lib/rhsm/",
            "/var/log/rhsm/rhsm.log",
            "/var/log/rhsm/rhsmcertd.log"])
        self.add_cmd_output([
            "subscription-manager list --installed",
            "subscription-manager list --available",
            "subscription-manager list --all --available",
            "subscription-manager list --consumed",
            "subscription-manager identity",
            "subscription-manager release --show",
            "subscription-manager release --list",
            "syspurpose show"
        ])
        self.add_cmd_output("rhsm-debug system --sos --no-archive "
                            "--no-subscriptions --destination %s"
                            % self.get_cmd_output_path())

        certs = glob.glob('/etc/pki/product-default/*.pem')
        self.add_cmd_output(["rct cat-cert %s" % cert for cert in certs])

    def postproc(self):
        passwdreg = r"(proxy_password(\s)*=(\s)*)(\S+)\n"
        repl = r"\1********\n"
        self.do_path_regex_sub("/etc/rhsm/rhsm.conf", passwdreg, repl)

# vim: et ts=4 sw=4
