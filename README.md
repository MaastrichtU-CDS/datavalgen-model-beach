# datavalgen-model-beach

This is an initial version of the BEACH (pydantic) model.

It's packaged in python package ready to be used by [datavalgen](https://github.com/mdw-nl/datavalgen)
– trivial little tool that just provides an "easier" way of validating data
against a pydantic model like the one include here.

## Validation Example

Scenario: You have some data in a csv that needs to be validated against the
schema included in this image. You have the data in a directory called `data`
and the file is called `tiny.csv`.

So, it looks like this:
```
$ tree data
data
└── tiny.csv

1 directory, 1 file
```

You can validate with something like:
```
$ docker run \
  --network none --rm --read-only --cap-drop=ALL --security-opt no-new-privileges=true --log-driver=none --user $(id -u):$(id -g) \
  -v ./data/tiny.csv:/data.csv:ro \
  ghcr.io/maastrichtu-cds/datavalgen-model-beach:put_version_here \
  validate
✅ No validation errors found.
```

> [!IMPORTANT]
> The options `--network none --rm --log-driver=none --read-only --cap-drop=ALL
> --security-opt no-new-privileges=true --user $(id -u):$(id -g)` run this image
> in a more locked-down way: they disable networking, prevent writes to the image
> filesystem, drop most extra operating system (OS) privileges, and tell Docker
> not to store container logs (you still see output in your terminal). This image
> is not expected to need any of those capabilities, so these flags are simply
> defense in depth, especially when you use real, private datasets. Please use them!
> And don't forget `:ro` either – validation will never need to modify your dataset.

> [!NOTE]
> You have to replace `put_version_here` with the actual version of the
> `datavalgen-model-beach` image you want to use. You can find the latest version
> [here](https://github.com/MaastrichtU-CDS/datavalgen-model-beach/pkgs/container/datavalgen-model-beach).
> (e.g. `ghcr.io/maastrichtu-cds/datavalgen-model-beach:v0.1.1`)

If there are errors, you will see output like this:
```
$ docker run \
  --network none --rm --read-only --cap-drop=ALL --security-opt no-new-privileges=true --log-driver=none --user $(id -u):$(id -g) \
  -v ./data/tiny.csv:/data.csv:ro \
  ghcr.io/maastrichtu-cds/datavalgen-model-beach:v0.1.0
  validate
❌ Line 2, column 'patient_t_stage': Input should be 'Tx', 'T1a', 'T1b', 'T1c', 'T2a', 'T2b', 'T3' or 'T4'.
   Got: 'T5c'.
❌ Line 11, column 'year_of_diagnosis': Input should be greater than or equal to 1890.
   Got: '1875'.
⚠️ Note: errors above contain your actual data values ("Got: .."). Do not share.
```

> [!NOTE]
> Note that "❌ Line 2" refers to the second line on the file itself, as you
> might see it in a simple editor. Line 1 would be the header, and line 2 would be
> the first row of data.

## Generating simple fake data
```
$ mkdir fakedata
$ docker run \
  --network none --rm --read-only --cap-drop=ALL --security-opt no-new-privileges=true --log-driver=none --user $(id -u):$(id -g)  \
  -v ./fakedata/:/data/ \
  ghcr.io/maastrichtu-cds/datavalgen-model-beach:v0.1.1 \
  generate -o fakebeach.csv
Changing ownership of output file to match data directory: /data (1000:1000)
Generated 10 rows to /data/fakebeach.csv in csv format.
$ wc -l fakedata/fakebeach.csv    # count rows + header
11 fakedata/fakebeach.csv
```

To validate it,
```
$ docker run \
  --network none --rm --read-only --cap-drop=ALL --security-opt no-new-privileges=true --log-driver=none --user $(id -u):$(id -g) \
  -v ./fakedata/fakebeach.csv:/data.csv:ro \
  ghcr.io/maastrichtu-cds/datavalgen-model-beach:v0.1.1 \
  validate
✅ No validation errors found.
```
