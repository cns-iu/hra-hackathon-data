import { existsSync, readFileSync, writeFileSync } from 'fs';
import { globSync } from 'glob';
import { basename, dirname, join } from 'path';
import sh from 'shelljs';

const JOURNAL = process.argv[2];
const OUT_DIR = process.argv[3];
const FILTER = process.argv.length === 5 ? process.argv[4] : undefined;

async function runQueries() {
  // Go through each query in queries, run them, and save out the csv report to ../data/reports/
  for (const queryFile of globSync('queries/reports/*/*.rq').sort()) {
    const reportName = basename(queryFile, '.rq');
    if (FILTER && !reportName.includes(FILTER)) {
      continue;
    }

    // Ensure output directory exists
    const reportDir = join(OUT_DIR, basename(dirname(queryFile)));
    sh.mkdir('-p', reportDir);

    const reportCsv = join(reportDir, `${reportName}.csv`);
    console.log('Creating report:', reportName);

    const query = readFileSync(queryFile).toString();
    writeFileSync(`${reportCsv}.rq`, query);

    const result = sh.exec(
      `blazegraph-runner --journal=${JOURNAL} select --outformat=json ${reportCsv}.rq ${reportCsv}.json`,
      { silent: true }
    );
    if (result.code) {
      console.log('[ERROR]', result.stderr);
    }
    sh.exec(`./src/sparql-json2csv.js ${reportCsv}.json ${reportCsv}`);
    sh.exec(`rm -f ${reportCsv}.json  ${reportCsv}.rq`);

    // If a post-processing SQL file is provided, run it to update the report
    if (existsSync(queryFile.replace('.rq', '.sql'))) {
      const sqlFile = queryFile.replace('.rq', '.sql');
      sh.exec(`./src/sql-select.sh ${sqlFile} ${reportCsv} ${reportCsv}`);
    }
  }
}

await runQueries();
