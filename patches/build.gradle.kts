group = "app.morphe"

patches {
    about {
        name = "Infinity+ Patches"
        description = "This app uses code from Patcheddit. To learn more, visit https://reddit.com/r/patcheddit"
        source = "https://github.com/Dabrogost/InfinityPlus-Patches"
        author = "Dabrogost (based on Patcheddit by wchill)"
        contact = "https://github.com/Dabrogost/InfinityPlus-Patches/issues"
        website = "https://github.com/Dabrogost/InfinityPlus-Patches"
        license = "GPL-3.0 with additional conditions under section 7; see LICENSE and NOTICE."
    }
}

dependencies {
    implementation(libs.gson)
    implementation(libs.guava)
    implementation(libs.morphe.patches.library)
    compileOnly(project(":patches:stub"))
}

kotlin {
    compilerOptions {
        freeCompilerArgs = listOf("-Xcontext-parameters")
    }
}
