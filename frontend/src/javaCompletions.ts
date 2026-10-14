import { completeAnyWord, snippetCompletion, type Completion, type CompletionContext, type CompletionResult } from '@codemirror/autocomplete'
import { javaLanguage } from '@codemirror/lang-java'
import { syntaxTree } from '@codemirror/language'

/**
 * Editor hints for Java, like the ones @codemirror/lang-python ships for Python (lang-java only highlights): keywords and
 * types, the calls a beginner of this course types most, members after a dot, and words already in the student's code.
 * No construct templates: a beginner should type `for` and `if` themselves.
 */
const words = (labels: string, type: string): Completion[] => labels.split(' ').map(label => ({ label, type }))

const KEYWORDS = words('abstract boolean break byte case catch char class continue default do double else extends false final finally float for if implements import instanceof int interface long new null private protected public return short static super switch this throw throws true try var void while', 'keyword')
const TYPES = words('String Integer Double Boolean Character Long Math System Scanner Object StringBuilder Arrays Collections List ArrayList LinkedList Map HashMap TreeMap LinkedHashMap Set HashSet TreeSet LinkedHashSet Exception RuntimeException ArithmeticException NumberFormatException IllegalArgumentException IllegalStateException ArrayIndexOutOfBoundsException IndexOutOfBoundsException NullPointerException', 'class')
const CALLS: Completion[] = [
  snippetCompletion('System.out.println(${})', { label: 'System.out.println', type: 'function', detail: 'вывод и перевод строки', boost: 2 }),
  snippetCompletion('System.out.print(${})', { label: 'System.out.print', type: 'function', detail: 'вывод без перевода строки', boost: 1 }),
]
const methods = (labels: string) => words(labels, 'method')
/** Members of the classes a beginner calls through the class name. */
const STATIC_MEMBERS: Record<string, Completion[]> = {
  System: [...words('out in', 'property'), ...methods('currentTimeMillis')],
  'System.out': methods('println print printf'),
  Math: [...methods('max min abs pow sqrt round floor ceil random'), ...words('PI', 'constant')],
  Integer: [...methods('parseInt valueOf toString'), ...words('MAX_VALUE MIN_VALUE', 'constant')],
  Double: [...methods('parseDouble valueOf toString'), ...words('MAX_VALUE MIN_VALUE', 'constant')],
  Long: methods('parseLong valueOf'),
  Boolean: methods('parseBoolean valueOf'),
  Character: methods('isDigit isLetter isLetterOrDigit isUpperCase isLowerCase isWhitespace toUpperCase toLowerCase getNumericValue'),
  String: methods('valueOf format join'),
  Arrays: methods('toString sort fill copyOf asList stream'),
  Collections: methods('sort reverse max min shuffle unmodifiableList'),
  List: methods('of copyOf'), Set: methods('of copyOf'), Map: methods('of entry copyOf'),
}
/** After a dot on a variable: the methods of strings, arrays, lists, sets, maps, Scanner and StringBuilder used in the course. */
const INSTANCE_MEMBERS: Completion[] = [
  ...methods('length charAt substring equals equalsIgnoreCase contains indexOf lastIndexOf toUpperCase toLowerCase trim isEmpty isBlank startsWith endsWith replace split compareTo repeat chars toCharArray'),
  ...methods('size get set add addAll remove removeIf clear contains containsKey containsValue put putIfAbsent getOrDefault keySet values entrySet getKey getValue sort forEach stream iterator first last'),
  ...methods('nextLine nextInt nextDouble next hasNext hasNextInt hasNextLine append insert reverse toString hashCode getClass getMessage'),
  ...words('length', 'property'),
]
const NO_HINTS = new Set(['StringLiteral', 'TextBlock', 'LineComment', 'BlockComment'])
const KNOWN = new Set([...KEYWORDS, ...TYPES, ...CALLS].map(c => c.label))

/** Inside a string or a comment: the syntax tree, and for a string still being typed (no closing quote yet) the line itself. */
function inTextOrComment(context: CompletionContext) {
  if (NO_HINTS.has(syntaxTree(context.state).resolveInner(context.pos, -1).name)) return true
  const line = context.state.doc.lineAt(context.pos)
  const before = line.text.slice(0, context.pos - line.from)
  let quotes = 0
  for (let i = 0; i < before.length; i++) { if (before[i] === '\\') i++; else if (before[i] === '"') quotes++ }
  return quotes % 2 === 1 || before.replace(/"(?:[^"\\]|\\.)*"/g, '""').includes('//')
}

function javaHints(context: CompletionContext): CompletionResult | null {
  if (inTextOrComment(context)) return null
  const member = context.matchBefore(/[A-Za-z_][\w.]*\.\w*$/)
  if (member) {
    const dot = member.text.lastIndexOf('.')
    const receiver = member.text.slice(0, dot)
    return { from: member.from + dot + 1, options: STATIC_MEMBERS[receiver] ?? INSTANCE_MEMBERS, validFor: /^\w*$/ }
  }
  const word = context.matchBefore(/\w+/)
  if (!word || (word.from === word.to && !context.explicit)) return null
  return { from: word.from, options: [...CALLS, ...KEYWORDS, ...TYPES], validFor: /^\w*$/ }
}
/** Words already typed in the code (variables, methods, fields) — but not inside strings and comments. */
async function codeWords(context: CompletionContext): Promise<CompletionResult | null> {
  if (inTextOrComment(context)) return null
  const result = await completeAnyWord(context)
  return result && { ...result, options: result.options.filter(o => !KNOWN.has(o.label)) }
}

export const javaCompletions = [javaLanguage.data.of({ autocomplete: javaHints }), javaLanguage.data.of({ autocomplete: codeWords })]
