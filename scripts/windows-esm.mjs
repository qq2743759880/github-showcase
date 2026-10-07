// Snap-X 0.7.0 core imports absolute Windows filenames as ESM specifiers.
// Convert only drive-qualified filenames; preserve its cache-busting query.
import { registerHooks } from 'node:module';
import { pathToFileURL } from 'node:url';
registerHooks({
  resolve(specifier, context, nextResolve) {
    if (/^[A-Za-z]:[\\/]/.test(specifier)) {
      const split = specifier.indexOf('?');
      const filename = split < 0 ? specifier : specifier.slice(0, split);
      const query = split < 0 ? '' : specifier.slice(split);
      specifier = pathToFileURL(filename).href + query;
    }
    return nextResolve(specifier, context);
  }
});
