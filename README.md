``SchemathesisLibrary`` is a [Robot Framework](https://robotframework.org/) library for fuzzing REST APIs by wrapping [Schemathesis](https://github.com/schemathesis/schemathesis) tool.

## Install 
```sh
pip3 install .
```

## Uninstall
```sh
pip3 uninstall robotframework-schemathesis
```

## Quick start
```robotframework
*** Settings ***
Library               SchemathesisLibrary    path_to_schema
Library               OperatingSystem


*** Variables ***
&{KWARGS}       base-url=http://ip:port/
...             cassette-path=cassette.yaml
...             hypothesis-max-examples=200
# ...             data-generation-method=negative


*** Test Cases ***
Schemathesis API Fuzz
    ${output}=    Run Fuzzing       &{KWARGS}   
    Create File    report.txt    ${output}
    &{dict}=    Get Failed Interactions
    Set Global Variable    &{FAILED_INT}    &{dict}
    

Schemathesis Replay Failed Testcases
    FOR    ${endpoint}    IN    @{FAILED_INT.keys()}
        FOR    ${id}    IN    @{FAILED_INT["${endpoint}"]}
            Replay Testcase    id=${id}
        END 
    END
```