import { loadQuartzConfig, loadQuartzLayout } from "./quartz/plugins/loader/config-loader"

import * as ExternalPlugin from "./.quartz/plugins";

ExternalPlugin.Explorer({
    sortFn: (a, b) => {
        return a.displayName.localeCompare(b.displayName);
    }
});



const config = await loadQuartzConfig()
export default config
export const layout = await loadQuartzLayout()
