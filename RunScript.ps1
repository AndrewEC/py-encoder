param(
    [ValidateSet(
        "All",
        "Audit",
        "Flake",
        "Install",
        "Tests"
    )]
    [string]$ScriptAction
)

Import-Module ./PyBuildScripts

Invoke-ActivateScript

switch ($ScriptAction) {
    "All" {
        Invoke-InstallScript
        Invoke-FlakeScript
        Invoke-TestScript 90 {
            coverage run `
                --omit=./encoder/tests/* `
                --source=encoder.lib `
                --branch `
                --module encoder.tests._run_all
        }
        Invoke-AuditScript
    }
    "Audit" { Invoke-AuditScript }
    "Flake" { Invoke-FlakeScript }
    "Install" { Invoke-InstallScript }
    "Tests" {
        Invoke-TestScript 90 {
            coverage run encoder.tests._run_all `
                --omit=./encoder/tests/* `
                --source=encoder.lib `
                --branch `
                --module
        }
    }
}
