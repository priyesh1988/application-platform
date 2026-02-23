{{- define "application-platform.name" -}}
application-platform
{{- end -}}

{{- define "application-platform.fullname" -}}
{{ include "application-platform.name" . }}
{{- end -}}
