
export class FormUtils {
    static focusNext(refs, ref) {
      if (refs.includes(ref)) {
        this.$refs[ref].focus();
      }
    }
}