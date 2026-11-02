/** @odoo-module **/

import { graphView } from "@web/views/graph/graph_view";
import { GraphRenderer } from "@web/views/graph/graph_renderer";
import { registry } from "@web/core/registry";
class ProjectReportGraphRenderer extends GraphRenderer {
    /**
     * Extract project_id from a domain array.
     *
     * @param {Array} domain
     * @returns {number|null}
     */
    _extractProjectId(domain) {
        for (const term of domain) {
            if (
                Array.isArray(term) &&
                term[0] === "project_id" &&
                term[1] === "="
            ) {
                return term[2];
            }
        }
        return null;
    }

    /**
     * Override graph clicks to redirect to project updates.
     *
     * @param {Array} domain
     */
    onGraphClickedFinal(domain) {
        const projectId = this._extractProjectId(domain);

        if (!projectId) {
            return super.onGraphClickedFinal(domain);
        }

        this.actionService.doAction("project.project_update_all_action", {
            additionalContext: { active_id: projectId },
        });
    }
}

export const projectReportGraphView = {
    ...graphView,
    Renderer: ProjectReportGraphRenderer,
};

registry.category("views").add("project_report_graph", projectReportGraphView);
