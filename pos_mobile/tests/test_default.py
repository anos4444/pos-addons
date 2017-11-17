# -*- coding: utf-8 -*-
import odoo.tests
from odoo.api import Environment


# tests is not work when pos_mobile and pos_restaurant was installed,
# but pos_mobile_restaurant was not installed so need
# to use post_install
@odoo.tests.common.at_install(False)
@odoo.tests.common.post_install(True)
class TestUi(odoo.tests.HttpCase):

    def test_01_pos_is_loaded(self):
        # see more https://odoo-development.readthedocs.io/en/latest/dev/tests/js.html#phantom-js-python-tests
        env = Environment(self.registry.test_cr, self.uid, {})

        # get exist pos_config
        main_pos_config = env.ref('point_of_sale.pos_config_main')
        # create new session and open it
        main_pos_config.open_session_cb()

        # needed because tests are run before the module is marked as
        # installed. In js web will only load qweb coming from modules
        # that are returned by the backend in module_boot. Without
        # this you end up with js, css but no qweb.
        env['ir.module.module'].search([('name', '=', 'pos_mobile')], limit=1).state = 'installed'
        self.registry.cursor().release()

        self.phantom_js(
            '/pos/web?m=1',

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".run('pos_mobile_tour')",

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".tours.pos_mobile_tour.ready",

            login="admin",
            timeout=240,
        )