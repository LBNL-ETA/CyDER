'use strict';

import { escapeHtml } from './escape-html.js';

// Require bootstrap-notify.js
export default function notifyError(restError) {
    switch(restError.xhr.status) {
    case 400:
        for(let field in restError.xhr.response) {
            let msg = '';
            for(let hint of restError.xhr.response[field])
                msg += '<br>' + escapeHtml(hint);
            $.notify({title: `<strong>${escapeHtml(field)}:</strong>`, message: msg},{type: 'danger'});
        }
        break;
    case 500:
        $.notify({title: `<strong>The server is in trouble :'(</strong><br>`, message: `It sounds really bad but a really devoted dude is working hard on it !`},{type: 'danger'});
        break;
    default:
        $.notify({title: `<strong>${escapeHtml(restError.xhr.statusText)}:</strong>`, message: escapeHtml(restError.xhr.response.detail)},{type: 'danger'});
        break;
    }
}
