import pytest

from aib.main import rewrite_manifest


@pytest.mark.parametrize("manifest,expected", [
    # Single input in rootfs with relative path.
    pytest.param({"pipelines": [
        {"name": "rootfs",
         "stages": [
             {"inputs": {'root_extra_content': {'mpp-embed': {'id': 'aefb4c0',
                                                              'path': 'files/relative/path/file1.txt'},
                                                  'origin': 'org.osbuild.source',
                                                  'type': 'org.osbuild.files'},
                        },
              "options": {'paths': [{'from': {'mpp-format-string': "input://root_extra_content/{embedded['aefb4c0']}"},
                                     'to': 'tree:///etc/destination/file1.conf'}]}
             },
         ]},
        {"name": "qm_rootfs"}
    ]}, [
        {'mpp-import-pipelines': {'path': 'include/build.ipp.yml'}},
        {"name": "rootfs",
         "stages": [
             {'mpp-eval': 'kernel_cmdline_stage'},
             {"inputs": {'root_extra_content': {'mpp-embed': {'id': 'aefb4c0',
                                                              'path': '/new/absolute/path/files/relative/path/file1.txt'},
                                                  'origin': 'org.osbuild.source',
                                                  'type': 'org.osbuild.files'},
                        },
              "options": {'paths': [{'from': {'mpp-format-string': "input://root_extra_content/{embedded['aefb4c0']}"},
                                     'to': 'tree:///etc/destination/file1.conf'}]}
             },
         ]},
        {"name": "qm_rootfs"},
        {'mpp-import-pipelines': {'path': 'include/image.ipp.yml'}}
    ], id="rootfs-single-relative"),
    # Multiple input in rootfs all with relative path.
    pytest.param({"pipelines": [
        {"name": "rootfs",
         "stages": [
             {"inputs": {'root_extra_content_0': {'mpp-embed': {'id': 'aefb4c0',
                                                                'path': '../files/relative/path/file1.txt'},
                                                  'origin': 'org.osbuild.source',
                                                  'type': 'org.osbuild.files'},
                        
                         'root_extra_content_1': {'mpp-embed': {'id': '6e3b505',
                                                                'path': 'files/relative/path/file2.txt'},
                                                  'origin': 'org.osbuild.source',
                                                  'type': 'org.osbuild.files'},
                        },
              "options": {'paths': [{'from': {'mpp-format-string': "input://root_extra_content_0/{embedded['aefb4c0']}"},
                                     'to': 'tree:///etc/destination/file1.conf'},
                                    {'from': {'mpp-format-string': "input://root_extra_content_1/{embedded['6e3b505']}"},
                                     'to': 'tree:///etc/destination/file2.conf'}]}
             },
         ]},
        {"name": "qm_rootfs"}
    ]}, [
        {'mpp-import-pipelines': {'path': 'include/build.ipp.yml'}},
        {"name": "rootfs",
         "stages": [
             {'mpp-eval': 'kernel_cmdline_stage'},
             {"inputs": {'root_extra_content_0': {'mpp-embed': {'id': 'aefb4c0',
                                                                'path': '/new/absolute/path/../files/relative/path/file1.txt'},
                                                  'origin': 'org.osbuild.source',
                                                  'type': 'org.osbuild.files'},
                         'root_extra_content_1': {'mpp-embed': {'id': '6e3b505',
                                                                'path': '/new/absolute/path/files/relative/path/file2.txt'},
                                                  'origin': 'org.osbuild.source',
                                                  'type': 'org.osbuild.files'}
                        },
              "options": {'paths': [{'from': {'mpp-format-string': "input://root_extra_content_0/{embedded['aefb4c0']}"},
                                     'to': 'tree:///etc/destination/file1.conf'},
                                    {'from': {'mpp-format-string': "input://root_extra_content_1/{embedded['6e3b505']}"},
                                     'to': 'tree:///etc/destination/file2.conf'}]}
             },
         ]},
        {"name": "qm_rootfs"},
        {'mpp-import-pipelines': {'path': 'include/image.ipp.yml'}}
    ], id="rootfs-multiple-relative"),
    # Multiple input in rootfs only last with relative path.
    pytest.param({"pipelines": [
        {"name": "rootfs",
         "stages": [
             {"inputs": {'root_extra_content_0': {'mpp-embed': {'id': 'aefb4c0',
                                                                'path': '/files/absolute/path/file1.txt'},
                                                  'origin': 'org.osbuild.source',
                                                  'type': 'org.osbuild.files'},
                        
                         'root_extra_content_1': {'mpp-embed': {'id': '6e3b505',
                                                                'path': '../files/relative/path/file2.txt'},
                                                  'origin': 'org.osbuild.source',
                                                  'type': 'org.osbuild.files'},
                        },
              "options": {'paths': [{'from': {'mpp-format-string': "input://root_extra_content_0/{embedded['aefb4c0']}"},
                                     'to': 'tree:///etc/destination/file1.conf'},
                                    {'from': {'mpp-format-string': "input://root_extra_content_1/{embedded['6e3b505']}"},
                                     'to': 'tree:///etc/destination/file2.conf'}]}
             },
         ]},
        {"name": "qm_rootfs"}
    ]}, [
        {'mpp-import-pipelines': {'path': 'include/build.ipp.yml'}},
        {"name": "rootfs",
         "stages": [
             {'mpp-eval': 'kernel_cmdline_stage'},
             {"inputs": {'root_extra_content_0': {'mpp-embed': {'id': 'aefb4c0',
                                                                'path': '/files/absolute/path/file1.txt'},
                                                  'origin': 'org.osbuild.source',
                                                  'type': 'org.osbuild.files'},
                        'root_extra_content_1': {'mpp-embed': {'id': '6e3b505',
                                                                'path': '/new/absolute/path/../files/relative/path/file2.txt'},
                                                  'origin': 'org.osbuild.source',
                                                  'type': 'org.osbuild.files'}
                        },
              "options": {'paths': [{'from': {'mpp-format-string': "input://root_extra_content_0/{embedded['aefb4c0']}"},
                                     'to': 'tree:///etc/destination/file1.conf'},
                                    {'from': {'mpp-format-string': "input://root_extra_content_1/{embedded['6e3b505']}"},
                                     'to': 'tree:///etc/destination/file2.conf'}]}
             },
         ]},
        {"name": "qm_rootfs"},
        {'mpp-import-pipelines': {'path': 'include/image.ipp.yml'}}
    ], id="rootfs-last-relative"),
    # Single input in qm_rootfs with relative path.
    pytest.param({"pipelines": [
        {"name": "rootfs"},
        {"name": "qm_rootfs",
         "stages": [
             {"inputs": {'qm_extra_content': {'mpp-embed': {'id': '292759f',
                                                            'path': '../files/relative/path/file1.txt'},
                                                  'origin': 'org.osbuild.source',
                                                  'type': 'org.osbuild.files'},
                        },
              "options": {'paths': [{'from': {'mpp-format-string': "input://qm_extra_content/{embedded['292759f']}"},
                                     'to': 'tree:///etc/destination/file1.conf'}]}
             },
         ]}
    ]}, [
        {'mpp-import-pipelines': {'path': 'include/build.ipp.yml'}},
        {"name": "rootfs"},
        {"name": "qm_rootfs",
         "stages": [
             {"inputs": {'qm_extra_content': {'mpp-embed': {'id': '292759f',
                                                                'path': '/new/absolute/path/../files/relative/path/file1.txt'},
                                                  'origin': 'org.osbuild.source',
                                                  'type': 'org.osbuild.files'},
                        },
              "options": {'paths': [{'from': {'mpp-format-string': "input://qm_extra_content/{embedded['292759f']}"},
                                     'to': 'tree:///etc/destination/file1.conf'}]}
             },
         ]},
        {'mpp-import-pipelines': {'path': 'include/image.ipp.yml'}}
    ], id="qm-rootfs-single-relative"),
    # A path not as part of an `mpp-embed` stage shall not be changed.
    # A non-realistic example used for the test purpose.
    pytest.param({"pipelines": [
        {"name": "rootfs"},
        {"name": "qm_rootfs",
         "stages": [
             {"inputs": {'qm_extra_content': {'path': '../files/relative/path/file1.txt',
                                              'origin': 'org.osbuild.source',
                                              'type': 'org.osbuild.files'},
                        },
              "options": {'paths': [{'from': {'mpp-format-string': "input://qm_extra_content/{embedded['292759f']}"},
                                     'to': 'tree:///etc/destination/file1.conf'}]}
             },
         ]}
    ]}, [
        {'mpp-import-pipelines': {'path': 'include/build.ipp.yml'}},
        {"name": "rootfs"},
        {"name": "qm_rootfs",
         "stages": [
             {"inputs": {'qm_extra_content': {'path': '../files/relative/path/file1.txt',
                                              'origin': 'org.osbuild.source',
                                              'type': 'org.osbuild.files'},
                        },
              "options": {'paths': [{'from': {'mpp-format-string': "input://qm_extra_content/{embedded['292759f']}"},
                                     'to': 'tree:///etc/destination/file1.conf'}]}
             },
         ]},
        {'mpp-import-pipelines': {'path': 'include/image.ipp.yml'}}
    ], id="qm-rootfs-relative-unchanged"),
    # Manifest already has a build pipeline imported.
    pytest.param({"pipelines": [
        {'mpp-import-pipelines': {'path': 'include/build.ipp.yml'}},
        {"name": "rootfs"},
        {"name": "qm_rootfs"}
    ]}, [
        {'mpp-import-pipelines': {'path': 'include/build.ipp.yml'}},
        {"name": "rootfs"},
        {"name": "qm_rootfs"},
        {'mpp-import-pipelines': {'path': 'include/image.ipp.yml'}}
    ], id="already-build-import"),
    # Manifest already has an image pipeline imported.
    pytest.param({"pipelines": [
        {"name": "rootfs"},
        {"name": "qm_rootfs"},
        {'mpp-import-pipelines': {'path': 'include/image.ipp.yml'}}
    ]}, [
        {'mpp-import-pipelines': {'path': 'include/build.ipp.yml'}},
        {"name": "rootfs"},
        {"name": "qm_rootfs"},
        {'mpp-import-pipelines': {'path': 'include/image.ipp.yml'}}
    ], id="already-image-import"),
    # The rootfs pipelines has empty stages declared, so appends 'kernel_cmdline_stage'.
    pytest.param({"pipelines": [
        {"name": "rootfs", "stages": []},
        {"name": "qm_rootfs"},
    ]}, [
        {'mpp-import-pipelines': {'path': 'include/build.ipp.yml'}},
        {"name": "rootfs", "stages": [{"mpp-eval": "kernel_cmdline_stage"}]},
        {"name": "qm_rootfs"},
        {'mpp-import-pipelines': {'path': 'include/image.ipp.yml'}}
    ], id="adds-kernel-cmdline-stage"),
    # The rootfs pipelines has no stages declared, do nothing with them.
    pytest.param({"pipelines": [
        {"name": "rootfs"},
        {"name": "qm_rootfs"},
    ]}, [
        {'mpp-import-pipelines': {'path': 'include/build.ipp.yml'}},
        {"name": "rootfs"},
        {"name": "qm_rootfs"},
        {'mpp-import-pipelines': {'path': 'include/image.ipp.yml'}}
    ], id="omits-kernel-cmdline-stage"),
])
def test_rewrite_manifest(manifest, expected):
    path = "/new/absolute/path"
    rewrite_manifest(manifest, path)
    assert manifest["pipelines"] == expected