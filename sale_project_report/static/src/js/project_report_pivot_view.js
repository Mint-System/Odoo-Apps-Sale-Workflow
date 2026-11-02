/** @odoo-module **/

import { pivotView } from "@web/views/pivot/pivot_view";
import { PivotRenderer } from "@web/views/pivot/pivot_renderer";
import { registry } from "@web/core/registry";
class ProjectReportPivotRenderer extends PivotRenderer {
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
     * Override cell clicks to redirect to project updates.
     *
     * @param {Object} cell
     */
    onOpenView(cell) {
        if (cell.value === undefined || this.model.metaData.disableLinking) {
            return;
        }

        const group = {
            rowValues: cell.groupId[0],
            colValues: cell.groupId[1],
            originIndex: cell.originIndexes[0],
        };
        const domain = this.model.getGroupDomain(group);
        const projectId = this._extractProjectId(domain);

        if (!projectId) {
            return super.onOpenView(cell);
        }

        this.actionService.doAction("project.project_update_all_action", {
            additionalContext: { active_id: projectId },
        });
    }
}

export const projectReportPivotView = {
    ...pivotView,
    Renderer: ProjectReportPivotRenderer,
};

registry.category("views").add("project_report_pivot", projectReportPivotView);
