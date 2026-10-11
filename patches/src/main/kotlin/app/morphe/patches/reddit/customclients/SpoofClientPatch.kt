/*
 * Copyright 2026 wchill.
 * https://github.com/wchill/patcheddit
 *
 * See the included NOTICE file for GPLv3 §7(b) and §7(c) terms that apply to this code.
 */

package app.morphe.patches.reddit.customclients

import app.morphe.patcher.patch.BytecodePatchBuilder
import app.morphe.patcher.patch.Option
import app.morphe.patcher.patch.bytecodePatch
import app.morphe.patcher.patch.stringOption

/**
 * Base class for patches that spoof the Reddit client.
 *
 * Supports a RedReader OAuth preset or a custom client ID.
 *
 * @param block The patch block. It is called with the client ID,
 * redirect URI, and user agent options.
 */
fun spoofClientPatch(
    name: String,
    description: String,
    block: BytecodePatchBuilder.(
        clientIdOption: Option<String>,
        redirectUriOption: Option<String>,
        userAgentOption: Option<String>
    ) -> Unit,
) = bytecodePatch(
    name = name,
    description = description,
    default = true
) {
    val clientIdOption = stringOption(
        key = "client-id",
        default = null,
        values = mapOf(
            "RedReader (shared client ID)" to "yH0aTnJEt6qUgGn835B4vg"
        ),
        title = "OAuth client ID",
        description = "Select the RedReader preset or enter your own " +
                "22-character Reddit OAuth client ID. Shared client IDs " +
                "may be restricted or stop working.",
        required = true,
        validator = { value ->
            !value.isNullOrBlank() &&
                    value.matches(Regex("^[\\w-]{22}$"))
        }
    )

    val redirectUriOption = stringOption(
        key = "redirect-uri",
        default = "redreader://rr_oauth_redir",
        values = null,
        title = "Redirect URI",
        description = "The Reddit OAuth redirect URI. " +
                "Defaults to RedReader's redirect URI. " +
                "Must match the selected client ID.",
        required = true,
    )

    val userAgentOption = stringOption(
        key = "user-agent",
        default = "org.quantumbadger.redreader/1.25.2",
        values = null,
        title = "User agent",
        description = "The Reddit API user agent. " +
                "Defaults to RedReader's user agent. " +
                "Custom client IDs may require a matching user agent.",
        required = true
    )

    block(
        clientIdOption,
        redirectUriOption,
        userAgentOption
    )
}

fun spoofClientPatch(
    block: BytecodePatchBuilder.(
        clientIdOption: Option<String>,
        redirectUriOption: Option<String>,
        userAgentOption: Option<String>
    ) -> Unit,
) = spoofClientPatch(
    name = "Spoof client",
    description = "Restores Infinity+ Reddit API functionality using " +
            "a selectable OAuth client ID preset or custom credentials.",
    block = block,
)
