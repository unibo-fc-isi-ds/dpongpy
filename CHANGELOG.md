## [1.1.0](https://github.com/gciatto/dpongpy/compare/1.0.0...1.1.0) (2024-10-29)

### Features

* support no gui and debug modes ([c9e23f6](https://github.com/gciatto/dpongpy/commit/c9e23f631436527a08d183270e28e6b3bd899eca))

### Dependency updates

* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.113 ([7155778](https://github.com/gciatto/dpongpy/commit/7155778b751c4da4354bc4d2ca94b8b8b3728f9a))
* **deps:** update npm to v10.9.0 ([cff8d66](https://github.com/gciatto/dpongpy/commit/cff8d66e605433b499235483e18c4738519291df))

### Bug Fixes

* update project description on poetry and pypi ([37aead4](https://github.com/gciatto/dpongpy/commit/37aead460d85b91696773ec5f28e5d9ae591bcd1))

### General maintenance

* improve readme ([6cc127c](https://github.com/gciatto/dpongpy/commit/6cc127c6a5c75399e6ba04c7706bfeebad61ca5f))
* private method names in remote.centralised ([8af2c5b](https://github.com/gciatto/dpongpy/commit/8af2c5beaa7f7ee6e0211678dfd4322868b01cc9))
* **release:** 1.0.1 [skip ci] ([c2c4889](https://github.com/gciatto/dpongpy/commit/c2c4889404f5508bd9892cc7be55344f31fcc1f4))

## [1.0.1](https://github.com/gciatto/dpongpy/compare/1.0.0...1.0.1) (2024-10-29)

### Dependency updates

* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.113 ([7155778](https://github.com/gciatto/dpongpy/commit/7155778b751c4da4354bc4d2ca94b8b8b3728f9a))
* **deps:** update npm to v10.9.0 ([cff8d66](https://github.com/gciatto/dpongpy/commit/cff8d66e605433b499235483e18c4738519291df))

### Bug Fixes

* update project description on poetry and pypi ([37aead4](https://github.com/gciatto/dpongpy/commit/37aead460d85b91696773ec5f28e5d9ae591bcd1))

### General maintenance

* improve readme ([6cc127c](https://github.com/gciatto/dpongpy/commit/6cc127c6a5c75399e6ba04c7706bfeebad61ca5f))

## 1.0.0 (2024-10-25)

### ⚠ BREAKING CHANGES

* remove support for python <3.10
* rename border->wall, Table->Board

### Features

* centralised works ([d5e6061](https://github.com/gciatto/dpongpy/commit/d5e6061e227fff1ad615682fc6dd50670ae5cb87))
* implement model ([006913f](https://github.com/gciatto/dpongpy/commit/006913fe0e236c173ae8aca59adc548f2efd3ebb))
* prototype view and controller ([6f02158](https://github.com/gciatto/dpongpy/commit/6f021583d41d558707a7c8bfd75657dec53bfe28))
* remove support for python <3.10 ([5bf2d7a](https://github.com/gciatto/dpongpy/commit/5bf2d7a179695fa906650a3da87cef090519e738))
* selectively get pygame events ([8fdaaaf](https://github.com/gciatto/dpongpy/commit/8fdaaaf0fa7ca43e10f4d35d5b197e4c6c645630))
* simulate package drop ([754b764](https://github.com/gciatto/dpongpy/commit/754b764a3bf45707f7b853e6b0ce92300c87a81a))
* test and improve model ([b8d378a](https://github.com/gciatto/dpongpy/commit/b8d378a3fb518021d407420a17a73135daed7be7))

### Bug Fixes

* control event (de)serialization ([45fd243](https://github.com/gciatto/dpongpy/commit/45fd2432bc5814040b4b238b8f31d2368e6dcbf5))
* deterministic assignment of paddle sides to keymaps ([6f55d0c](https://github.com/gciatto/dpongpy/commit/6f55d0c5fd6ba21547b5a7fb955e5e42547f30b7))
* echo client/server ([fe747dd](https://github.com/gciatto/dpongpy/commit/fe747dd5d15268fd7f40d9751a7de6fa65215d4d))
* graceful shutdown ([eec80e7](https://github.com/gciatto/dpongpy/commit/eec80e7036bfddd444931dc2a7f8f09ceeed406b))
* handle padles collisions ([521e04b](https://github.com/gciatto/dpongpy/commit/521e04b0c2b53a52e5815991bca79627ff727b6c))
* improve model ([b3d173b](https://github.com/gciatto/dpongpy/commit/b3d173bb89919ac0829f8d510b1c5c959adbc9fd))
* make coordinator and terminal stop in case of communication exception ([4f21e51](https://github.com/gciatto/dpongpy/commit/4f21e5119da9fb7f45a6151f4408d1e39153f368))
* make remote game updates async ([3c43703](https://github.com/gciatto/dpongpy/commit/3c43703b7b774d0e23ffe4fc8766a7aa41975fea))
* management of keymaps ([a3f1fd0](https://github.com/gciatto/dpongpy/commit/a3f1fd04c184c11cd437da0745c067f72473bd17))
* paddle commands initialization works on local too ([c4fc741](https://github.com/gciatto/dpongpy/commit/c4fc74132f4385ee7277bb9aa96577886eba26c8))
* remote main package import ([539ee3f](https://github.com/gciatto/dpongpy/commit/539ee3f6d6f380ec486cf3fc0be832db7b3a4fcf))
* server-side if selection ([3b96060](https://github.com/gciatto/dpongpy/commit/3b9606013406a04330793db8eeb8dd94af330187))
* several minor improvements to code structure ([728ad1d](https://github.com/gciatto/dpongpy/commit/728ad1d6bca63dbb7bfefc005190c97241b55635))
* udp handles socket close ([85df459](https://github.com/gciatto/dpongpy/commit/85df4591d8cf99a2f323398e2d8a816a2ab41d68))
* use finally to gracefully handle exceptions in game loop ([7228603](https://github.com/gciatto/dpongpy/commit/722860372e8464a257b54db2761cd321f2cb517a))
* view does not use python Protocols (which work differently on win) ([0273aa3](https://github.com/gciatto/dpongpy/commit/0273aa33ac9a527d52312fff6ac02b139d8e8de2))
* wrong type annotation in ControlEvent.is_control_event ([bec24e7](https://github.com/gciatto/dpongpy/commit/bec24e7943857df67758f2ba572fed447046beae))

### Tests

* fix unit tests ([e4c2ed8](https://github.com/gciatto/dpongpy/commit/e4c2ed8d72f764013fc5ae51ff40fd086600cdaa))
* test presentation ([7ac9994](https://github.com/gciatto/dpongpy/commit/7ac99940639f42dbbe92c6ff00827b1a3965e6d5))
* udp facilities ([4697570](https://github.com/gciatto/dpongpy/commit/4697570d61a163fc0d16d71b43b9d9654bf6350d))

### General maintenance

* **ci:** fix github release to include wheels ([020d1c3](https://github.com/gciatto/dpongpy/commit/020d1c38492fd720f1e34c73ba5f14e60992d520))
* consistent ellipsis in Client ([eb6a4de](https://github.com/gciatto/dpongpy/commit/eb6a4def0840ea2f49b8dfe1cc4638780a546fe2))
* log pong status override ([c3875f5](https://github.com/gciatto/dpongpy/commit/c3875f5ca79827b5721edf8870028886ac03ae4d))
* **release:** disable release on pypi ([0f85d8d](https://github.com/gciatto/dpongpy/commit/0f85d8da0d166cbbc7cf5de1138ee1ebb3d89c94))
* remove unused import ([34c4fb7](https://github.com/gciatto/dpongpy/commit/34c4fb71d47f43f3e212074a0bc878f5af3203bb))
* remove useless files ([610ef5a](https://github.com/gciatto/dpongpy/commit/610ef5a7869f2e248370bb76f8166fd35058a45f))
* rename project accordingly ([3f9124e](https://github.com/gciatto/dpongpy/commit/3f9124ee310597087ded03ffbf622914bb5adeb0))
* **style:** fix style to make mypy happy ([e0b64e7](https://github.com/gciatto/dpongpy/commit/e0b64e7d58a23bcc903c2a0609384a03b90aa38b))
* **style:** remove useless comments in dpongpy ([3b521f7](https://github.com/gciatto/dpongpy/commit/3b521f75d9a0a84423458ff4411f79b7744fc086))

### Refactoring

* avoid code repetition in udp ([609efe4](https://github.com/gciatto/dpongpy/commit/609efe425de89e27a47b4c6f7838606829fa2e2e))
* better field naming in PongCoordinator ([e4e11e0](https://github.com/gciatto/dpongpy/commit/e4e11e0305c84fc57dbb972b70298b3448c41e56))
* factorise main ([ea4ff4c](https://github.com/gciatto/dpongpy/commit/ea4ff4c30a7c9a13f0b41e42240b9a2ae2d693b9))
* rename border->wall, Table->Board ([ac82620](https://github.com/gciatto/dpongpy/commit/ac82620b8be11b55252a210b91ed14481915a45c))

## [2.1.6](https://github.com/aequitas-aod/template-python-project-poetry/compare/2.1.5...2.1.6) (2024-07-03)


### Bug Fixes

* **ci:** test release on all branches (use cmdline) ([db73c87](https://github.com/aequitas-aod/template-python-project-poetry/commit/db73c87689116f79322da3257813ea3327ccb922))

## [2.1.5](https://github.com/aequitas-aod/template-python-project-poetry/compare/2.1.4...2.1.5) (2024-07-03)


### Bug Fixes

* **ci:** test release on all branches ([f8ea880](https://github.com/aequitas-aod/template-python-project-poetry/commit/f8ea8807885441d52db8891f65e702e592ad412f))

## [2.1.4](https://github.com/aequitas-aod/template-python-project-poetry/compare/2.1.3...2.1.4) (2024-07-03)


### Dependency updates

* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.86 ([4bcc762](https://github.com/aequitas-aod/template-python-project-poetry/commit/4bcc7626f5b8643a7381b0c9c71b3d7a20a91ed1))


### Bug Fixes

* **deps:** update dependency scikit-learn to v1.5.1 ([edd9a84](https://github.com/aequitas-aod/template-python-project-poetry/commit/edd9a8415a5caaa2a64038a15c73cb4715e95765))


### Revert previous changes

* Revert "chore(deps): update dependency semantic-release-preconfigured-convent…" ([a51ce70](https://github.com/aequitas-aod/template-python-project-poetry/commit/a51ce70691409b04ea0948bb5cda8c562486b323))


### General maintenance

* improve readme ([9d62046](https://github.com/aequitas-aod/template-python-project-poetry/commit/9d620463be3b80a0da0a575bacbf9c3cce943982))

## [2.1.3](https://github.com/aequitas-aod/template-python-project-poetry/compare/2.1.2...2.1.3) (2024-07-03)


### Bug Fixes

* split prepare and publish phases in semantic-release ([d01a515](https://github.com/aequitas-aod/template-python-project-poetry/commit/d01a515d42e7666e13feea1489e934e84d0c06bd))

## [2.1.2](https://github.com/aequitas-aod/template-python-project-poetry/compare/2.1.1...2.1.2) (2024-07-03)


### Bug Fixes

* **ci:** pypi credentials ([42aa559](https://github.com/aequitas-aod/template-python-project-poetry/commit/42aa559de022c8a9381779d47750428195f708d8))

## [2.1.1](https://github.com/aequitas-aod/template-python-project-poetry/compare/2.1.0...2.1.1) (2024-07-03)


### Bug Fixes

* rename step in ci just to trigger new release ([d7f1d15](https://github.com/aequitas-aod/template-python-project-poetry/commit/d7f1d15e0bb590431099752e0b8529d9934df062))

## [2.1.0](https://github.com/aequitas-aod/template-python-project-poetry/compare/2.0.0...2.1.0) (2024-07-03)


### Features

* **ci:** add preliminary static checks and coverage before testing ([8566322](https://github.com/aequitas-aod/template-python-project-poetry/commit/8566322028fcfa92188be58627b13362dfa9b106))

## [2.0.0](https://github.com/aequitas-aod/template-python-project-poetry/compare/1.0.1...2.0.0) (2024-07-03)


### ⚠ BREAKING CHANGES

* use poetry instead of setup.py

### Features

* use poetry instead of setup.py ([f8bcfa1](https://github.com/aequitas-aod/template-python-project-poetry/commit/f8bcfa14bf7992b16e77929b6f5112dd7f977383))


### Dependency updates

* **deps:** update dependency pandas to v2.2.1 ([be273ce](https://github.com/aequitas-aod/template-python-project-poetry/commit/be273ce0d591432389c5da7d8bee343079db4871))
* **deps:** update dependency pandas to v2.2.2 ([dd4507a](https://github.com/aequitas-aod/template-python-project-poetry/commit/dd4507a5ae73bd2019729786dcbadb051a024049))
* **deps:** update dependency scikit-learn to v1.4.1.post1 ([d24ef8b](https://github.com/aequitas-aod/template-python-project-poetry/commit/d24ef8bc4bedf055630f95eb04a6db1833b3d4d7))
* **deps:** update dependency scikit-learn to v1.4.2 ([613452a](https://github.com/aequitas-aod/template-python-project-poetry/commit/613452a825e12cb0f5f2962e6ba5dd22dadf058a))
* **deps:** update dependency scikit-learn to v1.5.0 ([6d42082](https://github.com/aequitas-aod/template-python-project-poetry/commit/6d4208275a45736a4d4161dc88324aa3f6ca2b86))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.86 ([847ef5a](https://github.com/aequitas-aod/template-python-project-poetry/commit/847ef5a1ee00d72a7eb330d7f089c3130ced26ff))
* **deps:** update node.js to 20.12 ([2ffe13a](https://github.com/aequitas-aod/template-python-project-poetry/commit/2ffe13aeba2daea05735531926badafc0c6e78e2))
* **deps:** update node.js to 20.13 ([65182e8](https://github.com/aequitas-aod/template-python-project-poetry/commit/65182e88da58a8ad06bffb712572e388309767c2))
* **deps:** update node.js to 20.14 ([a132a42](https://github.com/aequitas-aod/template-python-project-poetry/commit/a132a42cf67d01fdf79778ffde824fb3300527ac))
* **deps:** update node.js to 20.15 ([76a552b](https://github.com/aequitas-aod/template-python-project-poetry/commit/76a552bc42965f6ee23754065b2673403b26a91c))


### General maintenance

* **release:** simplify renovate conf ([23da9b6](https://github.com/aequitas-aod/template-python-project-poetry/commit/23da9b61d38adbe974c53240f05fb71ea685fb03))

## [1.0.1](https://github.com/aequitas-aod/template-python-project/compare/1.0.0...1.0.1) (2024-02-02)


### Dependency updates

* **deps:** update dependency pandas to v2.1.2 ([8fe0d36](https://github.com/aequitas-aod/template-python-project/commit/8fe0d36a83c74ff23c059735a69f91ebef4904f3))
* **deps:** update dependency pandas to v2.1.3 ([27eb2b6](https://github.com/aequitas-aod/template-python-project/commit/27eb2b6e5cd7bdac497412095bdd71ee8bc9f12c))
* **deps:** update dependency pandas to v2.1.4 ([cd2b1d4](https://github.com/aequitas-aod/template-python-project/commit/cd2b1d4c3d22d352a89d57794402df9c8779b5c6))
* **deps:** update dependency pandas to v2.2.0 ([b8df6b1](https://github.com/aequitas-aod/template-python-project/commit/b8df6b14bdb94a9e4d290a67ae9090227da61d29))
* **deps:** update dependency scikit-learn to v1.3.2 ([fe7eea2](https://github.com/aequitas-aod/template-python-project/commit/fe7eea22d078a77ed77477a78785c387953888f8))
* **deps:** update dependency scikit-learn to v1.4.0 ([85de0ed](https://github.com/aequitas-aod/template-python-project/commit/85de0ed24d38277ea86a7ac71781631c097e8aaf))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.69 ([fa07343](https://github.com/aequitas-aod/template-python-project/commit/fa07343c199db9cf3a0784abdf1858983f80392c))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.70 ([2f7eb9b](https://github.com/aequitas-aod/template-python-project/commit/2f7eb9b20f5fc44a154c18cdf4ddb413da9819fc))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.71 ([e7efd4f](https://github.com/aequitas-aod/template-python-project/commit/e7efd4f39ac7396621ae9a7182c42975d8756476))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.72 ([17cd38c](https://github.com/aequitas-aod/template-python-project/commit/17cd38c5f6969e7be37be61087c63047d462e00a))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.73 ([ceba297](https://github.com/aequitas-aod/template-python-project/commit/ceba297fb66930fa41cfcc36794f37b16d041c60))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.74 ([a7c030d](https://github.com/aequitas-aod/template-python-project/commit/a7c030de41394700cc0cec89358e59a3709377b2))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.75 ([21e6b9a](https://github.com/aequitas-aod/template-python-project/commit/21e6b9af441d069af6c13ccbd55bad63d4a9a841))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.76 ([fcf51ce](https://github.com/aequitas-aod/template-python-project/commit/fcf51ce4d1048739ca4933ef56cefe69b1f25bb9))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.77 ([24c1ad5](https://github.com/aequitas-aod/template-python-project/commit/24c1ad5c7c2a6df6f8519c4bd3bfd9892cac7bdd))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.78 ([4881854](https://github.com/aequitas-aod/template-python-project/commit/488185409ad1263b83838fba5b07136517c9fe52))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.79 ([b09d25f](https://github.com/aequitas-aod/template-python-project/commit/b09d25f30d81f9bc22cee76f3cf2fe72e1589e62))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.80 ([d9e55c5](https://github.com/aequitas-aod/template-python-project/commit/d9e55c51fa21cf880450cbeee619cca167e55cec))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.81 ([d2608f8](https://github.com/aequitas-aod/template-python-project/commit/d2608f87dc1bb2554c4db8bd8fe57fb75512efdb))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.82 ([22b0719](https://github.com/aequitas-aod/template-python-project/commit/22b0719f19296441890e9e6f122df45efd5e095e))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.83 ([8f2ec20](https://github.com/aequitas-aod/template-python-project/commit/8f2ec20935428b99b28d412040689e56fa30a07e))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.84 ([cb92e70](https://github.com/aequitas-aod/template-python-project/commit/cb92e703568dbf402c51434c510fd97cb6946c52))
* **deps:** update dependency semantic-release-preconfigured-conventional-commits to v1.1.85 ([f05865d](https://github.com/aequitas-aod/template-python-project/commit/f05865d98e638d8c7192bfdb360898b7152400f9))
* **deps:** update node.js to 20.10 ([f393b2a](https://github.com/aequitas-aod/template-python-project/commit/f393b2a2fb2d3aa98b5c5a969ef4df442d5c79de))
* **deps:** update node.js to 20.11 ([63410da](https://github.com/aequitas-aod/template-python-project/commit/63410da68d5122d155caac39b6f99de19d619825))
* **deps:** update node.js to 20.9 ([d107ca2](https://github.com/aequitas-aod/template-python-project/commit/d107ca20dd8414ef39ab6b6b95740b3ae2c75f16))
* **deps:** update node.js to v20 ([61b7e25](https://github.com/aequitas-aod/template-python-project/commit/61b7e250a9afe02465f435c6b709b2fcc872e338))
* **deps:** update python docker tag to v3.12.0 ([b123d48](https://github.com/aequitas-aod/template-python-project/commit/b123d4847e25cc94e86faf1f5ec37a4e0b54e46d))
* **deps:** update python docker tag to v3.12.1 ([ac01a01](https://github.com/aequitas-aod/template-python-project/commit/ac01a014b54008d5c7af4916880413ba864f9a33))


### Bug Fixes

* **release:** include .python-version in MANIFEST.in ([9d794fa](https://github.com/aequitas-aod/template-python-project/commit/9d794faac19b032c5a0f149c3e5e44df018db17b))


### Build and continuous integration

* **deps:** update actions/setup-node action to v4 ([45c9acd](https://github.com/aequitas-aod/template-python-project/commit/45c9acdfed764240e4e150e65a4507205537a16a))
* **deps:** update actions/setup-python action to v5 ([66921e3](https://github.com/aequitas-aod/template-python-project/commit/66921e3580f3223689adf1665a323befbd9b3272))

## 1.0.0 (2023-10-12)


### Features

* add renaming script ([ed33dbc](https://github.com/aequitas-aod/template-python-project/commit/ed33dbc03a68a605e6df7a9465c6985ec9d1e130))
* first commit ([6ddc082](https://github.com/aequitas-aod/template-python-project/commit/6ddc08296facfe64fe912fcd00a255adb2806193))


### Dependency updates

* **deps:** node 18.18 ([73eec49](https://github.com/aequitas-aod/template-python-project/commit/73eec49c6fc53fe3158a0b94be99dcaf6eb328eb))
* **deps:** update dependencies ([0be2f8d](https://github.com/aequitas-aod/template-python-project/commit/0be2f8deb9b8218e509ea0926ceeb78a7a2baa70))
* **deps:** update python docker tag to v3.11.6 ([199ffe6](https://github.com/aequitas-aod/template-python-project/commit/199ffe6a498c6b26d358d97ac2ef7046da68e268))


### Bug Fixes

* readme ([f12fb0b](https://github.com/aequitas-aod/template-python-project/commit/f12fb0b17c08a18a7e145199234dc38d43fd0ddb))
* release workflow ([9c84ec1](https://github.com/aequitas-aod/template-python-project/commit/9c84ec1497a1f8c6c438a248107746df0fa7c612))
* renovate configuration ([0db8978](https://github.com/aequitas-aod/template-python-project/commit/0db89788ad8bef935fa97b77e7fa05aca749da28))


### Build and continuous integration

* enable semantic release ([648759b](https://github.com/aequitas-aod/template-python-project/commit/648759ba41fda0cad343493709a57bcb908f7229))
* fix release by installing correct version of node ([d809f17](https://github.com/aequitas-aod/template-python-project/commit/d809f17fc96c7295e0ec526161a56f558d49aa47))


### General maintenance

* **ci:** dry run release on testpypi for template project ([b90a25a](https://github.com/aequitas-aod/template-python-project/commit/b90a25a0f1f439e0bf548eec0bfae21b1f8c44b1))
* **ci:** use jq to parse package.json ([66af494](https://github.com/aequitas-aod/template-python-project/commit/66af494bc406d4b9b649153f910016cceb1b63ce))
* initial todo-list ([154e024](https://github.com/aequitas-aod/template-python-project/commit/154e024ac1bb8a1f1c99826ab2ed6a28e703a513))
* remove useless Dockerfile ([0272af7](https://github.com/aequitas-aod/template-python-project/commit/0272af71647e254f7622d38ace6000f0cbc7f17d))
* write some instructions ([7da9554](https://github.com/aequitas-aod/template-python-project/commit/7da9554a6e458c5fc253a222b295fbeb6a7862ec))
