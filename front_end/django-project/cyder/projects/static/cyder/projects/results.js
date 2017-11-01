class ProjectResults extends View {
    constructor(el) {
        super(el, 'div');
        this.project = null;
    }
    _getProject() {
        if(this._projectProm)
            return this._projectProm;
        else
            return Promise.resolve(this.project);
    }
    loadProject(projectId) {
        this._projectProm = (async () => {
            this.project = await CyderAPI.smartRest('GET', `/api/projects/${projectId}/`);
            this._projectProm = null;
        })();
        return this._getProject().then(() => { this.render() });
    }
    get _template() {
        return `
        <h1>Results</h1>
        <h4>Project: ${this.project.name}</h4>
        <br>
        <table class="table">
            <thead>
                <tr>
                  <th scope="col">Property</th>
                  <th scope="col">Value</th>
                </tr>
            </thead>
            <tbody>
                ${ FOREACH(this.project.results, (prop, value) =>
                    `<tr>
                        <td>${prop}</td>
                        <td>${value}</td>
                    </tr>`
                )}
            </tbody>
        </table>`;
    }
}
