
## General questions {#general}

### **Q:** Virus warnings in Windows Defender or Antivirus {#antivirus}

This is a complex topic to explain or not sound suspicious, bear with me - [Tremeschin](https://github.com/Tremeschin) - here.

:material-arrow-right: The short answer is to **only run executables from trusted sources**. There is nothing inherently malicious with my side of the packaging solution - you can read and verify the full [source code](https://github.com/BrokenSource/Pyaket), in fact, you can destroy my whole carreer[^carreer] if you find something of bad faith in there!

[^carreer]: Not something particurarly of my interest and professionalism - [reductio ad absurdum](https://en.wikipedia.org/wiki/Reductio_ad_absurdum).

!!! note "**Note:** I have no control or responsibility over what others use the project for"
    Similar to how a streaming platform or messaging app can't be held responsible for the shared content to an extent, other projects using pyaket (why you're reading this) requires your own judgement and benefit of the doubt.

#### Antivirus heuristics {#antivirus-heuristics}

Out of pure necessity for features to work, like bundling uv, python, script files, wheels, etc. some antivirus [heuristics](https://en.wikipedia.org/wiki/Heuristic) may detect the executables as malicious for a couple of reasons:

- Windows and Chrome knows every file you download or execute: A project getting popular or the rush to get a new release can have thousands of downloads pretty quickly. That's a sign of self-replication and fast spread, which will likely get automatically blocked.

- Better be safe than sorry, if something is half _sketchy_ better avoid it - this is a rule for life too. Microsoft and/or the AV are trying to protect users from their own mistakes, being strong on it as the platform is filled with non-technical users with malware targetting them {>>fair<<}

- Parts of the compiled rust code _can be similar_ to a known virus, as the language itself can be used to write malware (like any others), which will share many common community libraries source code, such as networking, compression, etc. {>>false positive<<}

- Pyaket bundles compressed files with code and tools, then calls external programs to install the project and run python. While this is something to **always** lookout for, as it can be seen as obfuscation or red flags, it's unavoidable for the scope and technology of the project.

Moral of the story, [correlation ≠ causation](https://en.wikipedia.org/wiki/Correlation_does_not_imply_causation), trust your sources.

#### Code signing {#code-signing}

!!! quote "How stuff like a browser, a game, steam, discord, etc. don't get flagged?"

The answer is [code signing](https://en.wikipedia.org/wiki/Code_signing), similar to how websites gets their [`https`](https://en.wikipedia.org/wiki/Let%27s_Encrypt) certificate.

:material-arrow-right: Essentially, files are _"sealed"_ with a digital signature before distribution, while still in a trusted environment from the developer. A certificate authority (like your government) maintains a list of trusted signatures that can be checked against (passports), but if the content differs from the original (fake photo or fingerprint) the signature will be deemed invalid.

- Many Open Source projects struggles due lack of funding, which makes it infeasible to even consider getting a certificate - as it's **not** an investment with direct returns.

- Most services that provides free signing for open source projects disallows selling the files, something pyaket advocates for the developer's hard work and paying the bills.

At its theoretical best, this is a way to gatekeep the bad actors out, as getting a signing certificate is very expensive, easily revoked if misused, requires sensitive information to become public such as address, phone number, legal name, etc. and might even not work properly in the end.

:material-arrow-right: **Note**: Funnily enough, this is a _non-issue_ on platforms with official package managers such as Linux distributions with educated users - an artificial problem created solely by closed systems.

<!-- Todo: Expand list, many places I've read through the years -->
<small>
Reference:
[(1)](https://news.ycombinator.com/item?id=19330062)
[(2)](https://www.reddit.com/r/csharp/comments/qh546a/do_we_really_need_to_buy_a_certificate_for_a/)
[(3)](https://github.com/pyinstaller/pyinstaller/issues/6754#issuecomment-1100821249)
</small>

## Technical questions
