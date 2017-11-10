class ProjectResults extends View {
    constructor(projectId, el) {
        super(el, 'div');
        this.loadProject(projectId);
    }
    loadProject(projectId, force = false) {
        this._projectId = projectId;
        let prom = CyderAPI.Project.get(this._projectId, force);
        if(prom instanceof Promise)
            this._ready = prom.then(() => { this.render() });
        else
            this._ready = Promise.resolve();
        this.render();
    }
    get _template() {
        let project = CyderAPI.Project.get(this._projectId);
        return `
        <h1>Results</h1>
        ${ IF(project instanceof Promise, () =>
            `<br>
            Loading...`
        , () =>
            `<h4>Project: ${escapeHtml(project.name)}</h4>
            <br>
            <table class="table">
                <thead>
                    <tr>
                      <th scope="col">Property</th>
                      <th scope="col">Value</th>
                    </tr>
                </thead>
                <tbody>
                    ${ FOREACH(project.results, (prop, value) =>
                        `<tr>
                            <td>${escapeHtml(prop)}</td>
                            <td>${escapeHtml(value)}</td>
                        </tr>`
                    )}
                </tbody>
            </table>`
        )}
        `;
    }
}
