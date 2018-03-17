import os
import sys
import traceback

def execute_bash(command):
    try:
        return os.system(command)
    except Exception:
        print(traceback.format_exc())


try:
    import jenkins
except Exception:
    execute_bash("sudo pip3 install python-jenkins")


job_xml = """ 

<project>
<actions/>
<description/>
<keepDependencies>false</keepDependencies>
<properties>
<com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty plugin="gitlab-plugin@1.5.3">
<gitLabConnection>gitlab</gitLabConnection>
</com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty>
</properties>
<scm class="hudson.scm.NullSCM"/>
<canRoam>true</canRoam>
<disabled>false</disabled>
<blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
<blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
<triggers/>
<concurrentBuild>false</concurrentBuild>
<builders>
<javaposse.jobdsl.plugin.ExecuteDslScripts plugin="job-dsl@1.67">
<scriptText>
    String private_token = "sc24K_e5avo6QjiF7G7c"
String ip = "http://172.17.0.2:80/"
		def jdata = new groovy.json.JsonSlurper().parseText(new URL("http://172.17.0.2:80/api/v3/projects?private_token="+private_token).text)
		jdata.each {
			String repo_url = it.ssh_url_to_repo
          	repo_url = repo_url.replace("git@gitlab.example.com:",ip)
            String proj =  repo_url.substring(repo_url.lastIndexOf('/') + 1);
			String project_name =  proj[0..-5]
            job(project_name) {
  
                description('A job for the project: ' + project_name)
                displayName(project_name)

                scm {
                    git {
                    branch('master')
                    remote { 
                        url(repo_url)
                        credentials('gitlab-root-user')
                    }
                    }
                }
  
                steps {
                    gradle('check')
                    gradle {
                    tasks('clean')
                    tasks('build')
                    switches('--stacktrace')
                    switches('--debug')
                
                    }
                    
                }
                
                publishers {
                    jacocoCodeCoverage {
                        execPattern '**/**.exec'
                        classPattern '**/classes'
                        sourcePattern '**/src/main/java'
                        exclusionPattern ''
                        inclusionPattern ''
                    }
                
                }
                
                triggers {
                        gitlabPush {
                            buildOnMergeRequestEvents(true)
                            buildOnPushEvents(true)
                        }
                    }
  
                authenticationToken('auhgtbereb675nksnwewrhbbe==')
  
            }
		}
</scriptText>
<usingScriptText>true</usingScriptText>
<sandbox>false</sandbox>
<ignoreExisting>false</ignoreExisting>
<ignoreMissingFiles>false</ignoreMissingFiles>
<failOnMissingPlugin>false</failOnMissingPlugin>
<unstableOnDeprecation>false</unstableOnDeprecation>
<removedJobAction>IGNORE</removedJobAction>
<removedViewAction>IGNORE</removedViewAction>
<removedConfigFilesAction>IGNORE</removedConfigFilesAction>
<lookupStrategy>JENKINS_ROOT</lookupStrategy>
</javaposse.jobdsl.plugin.ExecuteDslScripts>
</builders>
<publishers/>
<buildWrappers/>
</project>

 """

server = jenkins.Jenkins('http://localhost:8080',username='root',password='password')

server.create_job('master',job_xml)
server.build_job('master')