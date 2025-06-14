
- `gradlew publish`：发布所有发布
- `gradlew publishToMavenLocal`：发布到本地
- `gradlew publish[发布名]PublicationTo[仓库名]Repository`
	- 发布名：定义在`publishing.publications`
	- 仓库名：定义在`publishing.repositories`
	- 如`publishGprPublicationToGitHubPackagesRepository`



# 使用Github依赖
- 截止2025-4，Github依赖都需要认证，无论是谁，但是只要是公开就任何人都能下载

```kotlin
repositories {  
    maven{  
        name = "github-stream29"  
        url = uri("https://maven.pkg.github.com/stream29/streamlin")  
        credentials{  
            username = project.findProperty("GITHUB_PACKAGE_USERNAME") as String  
            password = project.findProperty("GITHUB_PACKAGE_RW_TOKEN") as String  
        }  
    }
}  
  
dependencies {  
    implementation("io.github.stream29:streamlin:2.5.1")  
}
```


# Gradle 本地install任务
```groovy
install.repositories.mavenInstaller.pom.project {
    name libName
    description libDescription
    url githubUrl
    groupId libGroup
    artifactId libArtifactId
    version libVersion
    packaging 'aar'

    scm {
        connection githubGit
        url githubUrl
    }
    licenses {
        license {
            name libLicenseName
            url libLicenseUrl
        }
    }

    developers {
        developer {
            id = 'natario'
            name 'Mattia Iavarione'
        }
    }
}
```


# Maven-Publish插件
```groovy
apply plugin: 'maven-publish'


// android 生成 bundleReleaseAar（artifact bundleReleaseAar）
apply plugin: 'com.android.library'
// java 生成 java（components.java）
apply plugin: 'java-library'


task sourcesJar(type: Jar) {
    archiveClassifier.set('sources')
    from android.sourceSets.main.java.srcDirs
}
task dokkaJar(type: Jar, dependsOn: dokka) {
    archiveClassifier.set('javadoc')
    from dokka.outputDirectory
}
artifacts {
    archives dokkaJar
    archives sourcesJar
}

//必须运行在 afterEvaluate
afterEvaluate {
    publishing {
        repositories {
	        // 发布到本地 Maven 仓库  
	        maven {
	            url = uri("file://${System.getenv("MAVEN_USER_HOME")}/repository") 
	        }
	        // 发布到Github Packages
            maven {
                name = "GitHubPackages"
                url = uri("https://maven.pkg.github.com/liruohrh/Transcoder")
                credentials {
                    username = project.findProperty("gpr.user") ?: System.getenv("USERNAME")
                    password = project.findProperty("gpr.key") ?: System.getenv("TOKEN")
                }
            }
        }
        publications {
            gpr(MavenPublication) {
                artifact bundleReleaseAar
                //同时发布javadoc和源码
                artifact javadocJar 
                artifact sourcesJar 
                pom {
                    artifactId = libArtifactId
                    groupId = libGroup
                    version = libVersion

                    name = libName
                    description = libDescription
                    url = githubUrl

                    licenses {
                        license {
                            name = libLicenseName
                            url = libLicenseUrl
                        }
                    }

                    developers {
                        developer {
                            id = 'natario'
                            name = 'Mattia Iavarione'
                        }
                        developer {
                            id = 'liruohrh'
                            name = 'LiRuo'
                        }
                    }

                    scm {
                        connection = "scm:git:https://github.com/liruohrh/Transcoder.git"
                        developerConnection = "scm:git:ssh://git@github.com:liruohrh/Transcoder.git"
                        url = "https://github.com/liruohrh/Transcoder"
                    }
                }
            }
        }
    }
}
```