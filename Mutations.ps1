$mutationCache = "./.mutmut-cache"
if (Test-Path $mutationCache) {
    Remove-Item $mutationCache
}
mutmut run
mutmut html
./html/index.html