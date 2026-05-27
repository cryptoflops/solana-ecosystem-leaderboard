const fs = require('fs');
const path = require('path');

function parseCSVLine(line) {
  const result = [];
  let current = '';
  let inQuotes = false;
  
  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === ',' && !inQuotes) {
      result.push(current);
      current = '';
    } else {
      current += char;
    }
  }
  result.push(current);
  return result;
}

function normalizeHandle(handleOrLink) {
  if (!handleOrLink) return "";
  let val = handleOrLink.trim().toLowerCase();
  if (val.startsWith('@')) return val;
  
  let match = val.match(/x\.com\/([a-zA-Z0-9_]+)/);
  if (match) return '@' + match[1];
  
  match = val.match(/twitter\.com\/([a-zA-Z0-9_]+)/);
  if (match) return '@' + match[1];
  
  return handleOrLink;
}

function main() {
  const workspaceDir = "/Users/psyhodivka/.gemini/antigravity-ide/scratch/solana-twitter-research";
  const csvPath = path.join(workspaceDir, "solana_influential_accounts.csv");

  // Read current CSV file
  const content = fs.readFileSync(csvPath, 'utf8');
  const lines = content.split('\n').filter(l => l.trim() !== "");
  const headers = parseCSVLine(lines[0]);
  
  const accounts = [];
  for (let i = 1; i < lines.length; i++) {
    const values = parseCSVLine(lines[i]);
    if (values.length < 4) continue;
    
    const row = {};
    for (let j = 0; j < headers.length; j++) {
      row[headers[j].trim()] = values[j] ? values[j].trim() : "";
    }
    accounts.push(row);
  }

  // Categories requested
  const CAT_FOUNDERS = "Founders of Solana projects";
  const CAT_OGS = "OGs (Original Gangsters/long-time contributors)";
  const CAT_BUILDERS = "Builders and developers";
  const CAT_RESEARCHERS = "Researchers";
  const CAT_BD = "Business Development (BD) roles";
  const CAT_MARKETING = "Marketing specialists";
  const CAT_IMPORTANT_OTHERS = "Anyone else deemed important for new founders to know";

  const cleanedAccounts = [];

  for (const acc of accounts) {
    const link = acc["Twitter Link"];
    const handle = normalizeHandle(link);
    const name = acc["Name"];
    const note = acc["Note"];
    const groupName = acc["Group Name"];

    let cleanCategory = CAT_IMPORTANT_OTHERS;

    // Direct mapping rules based on handle and descriptions
    const handleLower = handle.toLowerCase();
    const noteLower = note.toLowerCase();
    const nameLower = name.toLowerCase();

    // 1. Founders of Solana projects
    if (
      handleLower === "@toly" || 
      handleLower === "@rajgokal" ||
      handleLower === "@mert" ||
      handleLower === "@armaniferrante" ||
      handleLower === "@weremeow" ||
      handleLower === "@soleconomist" ||
      handleLower === "@y2kappa" ||
      handleLower === "@simkinstepan" ||
      handleLower === "@bennybitcoins" ||
      handleLower === "@cindyleowtt" ||
      handleLower === "@oritheorca" ||
      handleLower === "@rawfalafel" ||
      handleLower === "@0xshittrader" ||
      handleLower === "@jarxiao" ||
      handleLower === "@_ilmoi" ||
      handleLower === "@0xrwu" ||
      handleLower === "@baalazamon" ||
      handleLower === "@vibhu" ||
      handleLower === "@mattytay" ||
      handleLower === "@clayrobbins" ||
      handleLower === "@kylesamani" ||
      handleLower === "@tusharjain_" ||
      handleLower === "@highcoinviction" ||
      handleLower === "@ryanwatkins_" ||
      handleLower === "@nixxholas" ||
      handleLower === "@tarunchitra" ||
      noteLower.includes("founder") || 
      noteLower.includes("co-founder") || 
      noteLower.includes("ceo")
    ) {
      cleanCategory = CAT_FOUNDERS;
    }
    // 2. OGs
    else if (
      handleLower === "@solbigbrain" ||
      handleLower === "@blknoiz06" ||
      handleLower === "@_jackdunham" ||
      handleLower === "@solanafloor" ||
      handleLower === "@solanasean" ||
      handleLower === "@moonoverlord" ||
      handleLower === "@solanalegend" ||
      handleLower === "@solbuckets" ||
      handleLower === "@frankdegods" ||
      handleLower === "@cobie" ||
      noteLower.includes("og") ||
      noteLower.includes("veteran")
    ) {
      cleanCategory = CAT_OGS;
    }
    // 3. Builders and developers
    else if (
      handleLower === "@stephenakridge" ||
      handleLower === "@buffalu__" ||
      handleLower === "@danielfromjito" ||
      handleLower === "@brianlong" ||
      handleLower === "@laine_sa" ||
      handleLower === "@nickfrosty" ||
      handleLower === "@kiryl_sol" ||
      handleLower === "@solana_devs" ||
      handleLower === "@frankieisokay" ||
      handleLower === "@yver__" ||
      handleLower === "@0xsats" ||
      noteLower.includes("developer") ||
      noteLower.includes("devrel") ||
      noteLower.includes("builder") ||
      noteLower.includes("engineer")
    ) {
      cleanCategory = CAT_BUILDERS;
    }
    // 4. Researchers
    else if (
      handleLower === "@messaricrypto" ||
      handleLower === "@solanafm" ||
      handleLower === "@stepfinance_" ||
      handleLower === "@dunesolana" ||
      handleLower === "@tokenunlocks" ||
      handleLower === "@santiagorsantos" ||
      handleLower === "@spencernoon" ||
      handleLower === "@rektcapital" ||
      handleLower === "@0xliang" ||
      handleLower === "@helios_sol" ||
      handleLower === "@0xcheeezzyyyy" ||
      handleLower === "@zieeyer" ||
      noteLower.includes("research") ||
      noteLower.includes("analyst") ||
      noteLower.includes("analytics")
    ) {
      cleanCategory = CAT_RESEARCHERS;
    }
    // 5. BD Roles
    else if (
      handleLower === "@solanafndn" ||
      handleLower === "@superteam" ||
      handleLower === "@magiceden" ||
      handleLower === "@jupiterexchange" ||
      handleLower === "@phantom" ||
      handleLower === "@heliuslabs" ||
      handleLower === "@wormhole" ||
      handleLower === "@pythnetwork" ||
      handleLower === "@jitofdn" ||
      handleLower === "@kaminofinance" ||
      handleLower === "@mdomcahill" ||
      handleLower === "@jayantkrish" ||
      noteLower.includes("bd") ||
      noteLower.includes("business development") ||
      noteLower.includes("partnership")
    ) {
      cleanCategory = CAT_BD;
    }
    // 6. Marketing specialists
    else if (
      handleLower === "@solanasensei" ||
      handleLower === "@cozypront" ||
      handleLower === "@soljakey" ||
      handleLower === "@cryptoanglio" ||
      handleLower === "@leonardnftpage" ||
      handleLower === "@mortyweb3" ||
      handleLower === "@solananewton" ||
      handleLower === "@thesolanaboss" ||
      handleLower === "@solcommunityy" ||
      handleLower === "@crowdcreate_us" ||
      handleLower === "@akshaybd" ||
      handleLower === "@kashdhanda" ||
      handleLower === "@garrettharper_" ||
      handleLower === "@slorgoftheslugs" ||
      handleLower === "@lightspeedpod" ||
      handleLower === "@degennews" ||
      handleLower === "@solanadaily" ||
      noteLower.includes("marketing") ||
      noteLower.includes("media") ||
      noteLower.includes("podcast") ||
      noteLower.includes("community")
    ) {
      cleanCategory = CAT_MARKETING;
    }
    // 7. Anyone else
    else {
      cleanCategory = CAT_IMPORTANT_OTHERS;
    }

    cleanedAccounts.push({
      groupName: cleanCategory,
      link: link,
      name: name,
      note: note
    });
  }

  // Sort logically: Category first, then Name
  const categoryOrder = [
    CAT_FOUNDERS,
    CAT_OGS,
    CAT_BUILDERS,
    CAT_RESEARCHERS,
    CAT_BD,
    CAT_MARKETING,
    CAT_IMPORTANT_OTHERS
  ];

  cleanedAccounts.sort((a, b) => {
    const catIndexA = categoryOrder.indexOf(a.groupName);
    const catIndexB = categoryOrder.indexOf(b.groupName);
    
    if (catIndexA !== catIndexB) {
      return catIndexA - catIndexB;
    }
    return a.name.localeCompare(b.name);
  });

  // Write new CSV
  let csvContent = "Group Name,Twitter Link,Name,Note\n";
  for (const acc of cleanedAccounts) {
    // Format values to escape quotes/commas
    const escapeCSV = (str) => {
      if (str.includes(",") || str.includes("\"") || str.includes("\n")) {
        return `"${str.replace(/"/g, '""')}"`;
      }
      return str;
    };
    csvContent += `${escapeCSV(acc.groupName)},${escapeCSV(acc.link)},${escapeCSV(acc.name)},${escapeCSV(acc.note)}\n`;
  }

  fs.writeFileSync(csvPath, csvContent, 'utf8');
  console.log(`Successfully rewrote ${cleanedAccounts.length} cleaned and categorized accounts in ${csvPath}`);
}

main();
