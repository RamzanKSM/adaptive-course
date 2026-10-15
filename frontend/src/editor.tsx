import { java } from '@codemirror/lang-java'
import { python } from '@codemirror/lang-python'
import ReactMarkdown from 'react-markdown'
import { javaCompletions } from './javaCompletions'

// Stable references: a new extensions array on every render would make CodeMirror reconfigure the editor.
export const EDITOR_EXTENSIONS = { JAVA: [java(), javaCompletions], PYTHON: [python()] }
/** The editor's text when a task has no starter code. */
export const FALLBACK_CODE = {
  JAVA: 'public class Solution {\n    public static void main(String[] args) {\n        // Напишите решение здесь\n    }\n}\n',
  PYTHON: '# Напиши решение здесь\n',
}

export function Markdown({ children, inline = false }: { children: string; inline?: boolean }) {
  const content = <ReactMarkdown
    components={{
      p: ({ children: paragraphChildren }) => inline ? <>{paragraphChildren}</> : <p>{paragraphChildren}</p>,
      code: ({ className, children, node: _node, ...props }) => {
        const language = /language-(\w+)/.exec(className || '')?.[1]
        return language ? <code className={`language-${language}`}>{children}</code> : <code {...props}>{children}</code>
      },
    }}
  >{children}</ReactMarkdown>
  return inline ? <span className="markdown inline-markdown">{content}</span> : <div className="markdown">{content}</div>
}
