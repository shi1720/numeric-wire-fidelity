"""Download pinned public schemas; retain only data/ and provenance README."""
import argparse,hashlib,json,tarfile,tempfile,urllib.request
from pathlib import Path
REV='9a94995b9279ae3af3aed4b2629172790b968d14'
SHA='93392ae4b0ddd3459a7ce3369332ef7d0ea1efabda96b07d2accd8ff093fdb57'
URL='https://codeload.github.com/guidance-ai/jsonschemabench/tar.gz/'+REV
p=argparse.ArgumentParser();p.add_argument('--dest',default='../corpus');a=p.parse_args();dest=Path(a.dest);dest.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
 archive=Path(tmp)/'corpus.tar.gz';urllib.request.urlretrieve(URL,archive)
 assert hashlib.sha256(archive.read_bytes()).hexdigest()==SHA,'Archive hash mismatch'
 with tarfile.open(archive) as tar:
  for m in tar:
   if not m.isfile():continue
   parts=Path(m.name).parts
   if len(parts)<2 or '..' in parts:continue
   rel=Path(*parts[1:])
   if not ((parts[1]=='data' and m.name.endswith('.json')) or str(rel)=='README.md'):continue
   target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True)
   target.write_bytes(tar.extractfile(m).read())
manifest=json.loads((Path(__file__).resolve().parents[1]/'data/corpus_manifest.json').read_text())
for x in manifest:
 path=dest/'data'/x['file'];assert hashlib.sha256(path.read_bytes()).hexdigest()==x['sha256'],x['file']
print('Verified',len(manifest),'schema files at',dest.resolve())
