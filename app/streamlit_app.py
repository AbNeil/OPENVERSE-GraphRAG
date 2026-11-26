"""Reconstructed OPENVERSE demonstration interface; not the original October source."""
from pathlib import Path
import subprocess
import sys
import time
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'ragtest'
st.set_page_config(page_title='OPENVERSE Graph-RAG', layout='wide')
st.title('OPENVERSE Graph-RAG')
st.caption('Knowledge-grounded governance intelligence | Research demonstration')
st.info('Requires authorised indexed artifacts and a running local Ollama service. Outputs are not legal advice.')
with st.sidebar:
    st.header('Retrieval configuration')
    method = st.radio('Search method', ['local', 'global'])
    candidates = sorted((PROJECT / 'output').glob('*/artifacts'), reverse=True)
    default = str(candidates[0]) if candidates else ''
    data = st.text_input('Index artifact directory', value=default)
    level = st.number_input('Community level', min_value=0, value=2, step=1)
    timeout = st.number_input('Timeout (seconds)', min_value=30, max_value=3600, value=300, step=30)
question = st.text_area('Governance question', value='What governance issues arise from biometric authentication in virtual worlds?')
if st.button('Run query', type='primary'):
    if not question.strip():
        st.error('Enter a question.')
    elif not data.strip() or not Path(data).expanduser().is_dir():
        st.error('Select an existing index artifact directory.')
    elif not (ROOT / 'query.py').is_file():
        st.error('query.py is missing from the repository root.')
    else:
        cmd = [sys.executable, str(ROOT / 'query.py'), '--root', str(PROJECT), '--data', str(Path(data).expanduser().resolve()), '--method', method, '--community_level', str(level), '--', question.strip()]
        start = time.monotonic()
        try:
            with st.spinner('Executing GraphRAG query...'):
                result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=int(timeout), check=False)
            st.metric('Elapsed time (seconds)', round(time.monotonic()-start, 2))
            if result.returncode:
                st.error(f'Query failed (exit code {result.returncode}).')
            st.subheader('Actual CLI output')
            st.text(result.stdout or '(No standard output)')
            if result.stderr:
                with st.expander('Diagnostics', expanded=bool(result.returncode)):
                    st.code(result.stderr, language='text')
        except subprocess.TimeoutExpired:
            st.error('Query exceeded the configured timeout. No answer is claimed.')
        except OSError as exc:
            st.error(str(exc))
