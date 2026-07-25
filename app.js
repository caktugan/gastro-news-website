const stories = {
  vienna: [],
  austria: [
    {
      id: "vienna-dining-wave",
      edition: "Austria",
      topic: "Restaurants",
      location: "Vienna",
      time: "32 min ago",
      title: "Vienna’s next dining wave is moving beyond the Ring",
      deck: "Independent kitchens are choosing neighbourhood intimacy over grand dining rooms—and quietly changing how the city eats.",
      image: "./assets/vienna-kitchen.webp",
      sources: 8,
      initials: ["RP", "FS", "W"],
      brief: [
        "A cluster of chef-led openings is concentrating in Vienna’s outer inner districts, where smaller rooms and flexible menus reduce operating pressure.",
        "The new formats favour concise seasonal menus, counter seating and direct relationships with regional producers.",
        "Industry observers see the shift as a durable response to staffing and cost pressure—not simply a design trend."
      ],
      why: "The format changes the economics of opening a serious restaurant in Vienna. Smaller teams and rooms can lower risk while creating a more personal kind of hospitality, giving independent operators a credible alternative to high-capital fine dining.",
      sourceNames: ["Rolling Pin · Sample coverage", "Falstaff · Sample reporting", "Local operator statement"]
    },
    {
      id: "vienna-bakery-wave",
      edition: "Austria",
      topic: "Food & Wine",
      location: "Vienna",
      time: "1 hr ago",
      title: "Independent bakeries reshape Vienna’s morning ritual",
      deck: "A new generation of small bakeries is bringing milling, fermentation and neighbourhood identity back into focus.",
      image: "./assets/vienna-bakery.webp",
      sources: 5,
      initials: ["FS", "ST"],
      brief: [
        "New bakery concepts are pairing long-fermented bread with compact coffee and breakfast programmes.",
        "Operators are using visible production and direct grain sourcing to distinguish themselves from chain formats.",
        "Morning trade is becoming a meaningful all-day hospitality entry point rather than a standalone retail moment."
      ],
      why: "Bakery-led hospitality reaches customers more frequently than destination dining. That makes it an important testing ground for local sourcing, premium everyday pricing and smaller-footprint concepts.",
      sourceNames: ["Local reporting · Sample", "Producer interview · Sample", "Trade desk · Sample"]
    },
    {
      id: "wachau-harvest",
      edition: "Austria",
      topic: "Sustainability",
      location: "Wachau",
      time: "2 hrs ago",
      title: "Wachau growers prepare for a more compressed harvest",
      deck: "Vineyard teams are adapting staffing and cellar plans as ripening windows become harder to predict.",
      image: "./assets/wachau-vineyard.webp",
      sources: 6,
      initials: ["WV", "ÖW", "P"],
      brief: [
        "Growers are preparing for shorter picking windows across several terraced vineyard sites.",
        "More flexible seasonal staffing and faster grape transport are becoming operational priorities.",
        "Producers are also reassessing canopy management and water retention for future vintages."
      ],
      why: "Vintage conditions affect restaurant wine lists, release schedules and pricing well beyond the vineyard. Earlier operational signals help buyers plan allocations and communicate changes to guests.",
      sourceNames: ["Regional growers · Sample", "Wine trade desk · Sample", "Producer release · Sample"]
    },
    {
      id: "collective-agreement",
      edition: "Austria",
      topic: "Business",
      location: "Austria",
      time: "48 min ago",
      title: "Hospitality employers look for clarity on the next labour agreement",
      deck: "Scheduling, weekend pay and staff retention remain at the centre of the industry conversation.",
      image: null,
      sources: 11,
      initials: ["WK", "OR", "DS"],
      brief: [
        "Employer and employee representatives remain focused on predictable scheduling and compensation for high-demand periods.",
        "Independent operators say implementation details matter as much as headline wage changes.",
        "Recruitment pressure remains uneven, with regional and seasonal businesses facing distinct constraints."
      ],
      why: "Labour terms shape menu prices, opening hours and the viability of service formats. Clear rules allow operators to plan capacity instead of reacting week by week.",
      sourceNames: ["WKO · Sample coverage", "Public broadcaster · Sample", "Labour representative · Sample"]
    },
    {
      id: "alpine-hotel-menus",
      edition: "Austria",
      topic: "Restaurants",
      location: "Salzburg",
      time: "3 hrs ago",
      title: "Alpine hotels are giving their restaurants a life of their own",
      deck: "New dining identities are designed to attract local guests—not only overnight visitors.",
      image: "./assets/vienna-kitchen.webp",
      sources: 7,
      initials: ["HT", "RP", "FS"],
      brief: [
        "Hotels are separating restaurant brands from the parent property to build stronger local recognition.",
        "Street-facing entrances, independent booking and more focused menus are common parts of the shift.",
        "The strategy can smooth seasonal demand by adding a dependable local audience."
      ],
      why: "A restaurant that works as a local destination can diversify hotel revenue and strengthen year-round staffing. It also forces clearer positioning than the traditional all-purpose hotel dining room.",
      sourceNames: ["Hotel trade press · Sample", "Operator interview · Sample", "Regional desk · Sample"]
    },
    {
      id: "vegetable-led-menus",
      edition: "Austria",
      topic: "Food & Wine",
      location: "Graz",
      time: "4 hrs ago",
      title: "Vegetable-led menus move past the substitute mindset",
      deck: "Chefs are treating plants as the organising idea of a dish rather than an alternative version of it.",
      image: "./assets/live-fire.webp",
      sources: 4,
      initials: ["G", "FS"],
      brief: [
        "New menus are reducing their dependence on imitation proteins and focusing on technique, preservation and texture.",
        "Regional pulses, mushrooms and fermented vegetables are increasingly central to menu development.",
        "Operators report that clear culinary language performs better than dietary labelling alone."
      ],
      why: "The shift creates a broader audience than strictly vegan positioning and can improve ingredient flexibility. It also gives Austrian produce a stronger role in contemporary restaurant identity.",
      sourceNames: ["Chef interview · Sample", "Regional reporting · Sample", "Menu analysis · Sample"]
    },
    {
      id: "coffee-costs",
      edition: "Austria",
      topic: "Business",
      location: "Austria",
      time: "5 hrs ago",
      title: "Coffee operators rethink pricing without losing the daily guest",
      deck: "Smaller menus and clearer sourcing stories are emerging as cafés absorb another round of cost pressure.",
      image: null,
      sources: 9,
      initials: ["WK", "P", "K"],
      brief: [
        "Specialty operators are simplifying menus to protect quality and service speed.",
        "Many are pairing measured price changes with more explicit communication about sourcing and labour.",
        "Food attachments and retail beans remain important ways to improve the economics of each visit."
      ],
      why: "Coffee is one of hospitality’s most frequent price signals. How cafés communicate increases can influence broader customer expectations around quality, wages and ingredient costs.",
      sourceNames: ["Trade survey · Sample", "Operator interviews · Sample", "Market note · Sample"]
    }
  ],
  global: [
    {
      id: "live-fire-technique",
      edition: "Global",
      topic: "Restaurants",
      location: "Global",
      time: "24 min ago",
      title: "Live-fire cooking moves from theatre to technique",
      deck: "The next generation of open-fire restaurants is quieter, more precise and increasingly vegetable-led.",
      image: "./assets/live-fire.webp",
      sources: 14,
      initials: ["ET", "MG", "RB"],
      brief: [
        "Chefs are using coals and embers for controlled heat, preservation and texture rather than spectacle alone.",
        "New restaurant designs place fire at the centre while investing heavily in ventilation and energy efficiency.",
        "Vegetables and whole-animal cookery are giving the format a broader culinary vocabulary."
      ],
      why: "Live fire is maturing into an operating system rather than a visual theme. The most interesting concepts now connect technique, menu design and waste reduction in ways that can travel across markets.",
      sourceNames: ["Eater · Sample coverage", "Michelin Guide · Sample", "Restaurant trade press · Sample"]
    },
    {
      id: "shorter-tasting-menus",
      edition: "Global",
      topic: "Restaurants",
      location: "Europe",
      time: "1 hr ago",
      title: "The tasting menu gets shorter—and more confident",
      deck: "Leading restaurants are trading endurance for rhythm, giving guests fewer courses and clearer choices.",
      image: "./assets/vienna-kitchen.webp",
      sources: 10,
      initials: ["MG", "ET", "FT"],
      brief: [
        "Several ambitious restaurants are reducing course counts while protecting the narrative arc of the meal.",
        "Shorter formats improve table timing, labour planning and accessibility for guests.",
        "Optional additions are replacing rigid extended menus in many concepts."
      ],
      why: "Fine dining is responding to a guest who still wants craft but is more selective about time and spend. The operational benefits may make shorter formats more resilient as well as more welcoming.",
      sourceNames: ["Michelin Guide · Sample", "European food desk · Sample", "Restaurant interview · Sample"]
    },
    {
      id: "fermentation-labs",
      edition: "Global",
      topic: "Sustainability",
      location: "Copenhagen",
      time: "2 hrs ago",
      title: "Restaurant fermentation labs become shared infrastructure",
      deck: "Independent kitchens are pooling research, equipment and surplus produce instead of building isolated programmes.",
      image: "./assets/wachau-vineyard.webp",
      sources: 7,
      initials: ["MAD", "FC", "ET"],
      brief: [
        "Shared fermentation spaces are giving smaller restaurants access to equipment and food-safety expertise.",
        "The model creates a productive destination for seasonal surplus from farms and markets.",
        "Participants are developing shared base products while retaining distinct finishing techniques."
      ],
      why: "Shared production can turn sustainability from a branding promise into practical infrastructure. The model is especially relevant to cities with many small independent restaurants and strong regional farms.",
      sourceNames: ["Nordic food desk · Sample", "Research collective · Sample", "Chef statement · Sample"]
    },
    {
      id: "restaurant-groups-scale",
      edition: "Global",
      topic: "Business",
      location: "London",
      time: "46 min ago",
      title: "Restaurant groups pursue slower, more deliberate growth",
      deck: "Operators are prioritising repeatable culture and purchasing power over a rapid race for locations.",
      image: null,
      sources: 18,
      initials: ["CT", "RB", "FT"],
      brief: [
        "Several mid-sized groups are slowing openings to strengthen management pipelines and procurement.",
        "Smaller city clusters are preferred over widely dispersed portfolios.",
        "Leadership teams are treating training systems as a prerequisite for expansion rather than a later fix."
      ],
      why: "Measured growth suggests the sector is absorbing lessons from the last expansion cycle. The strongest groups may look less like property portfolios and more like durable operating cultures.",
      sourceNames: ["The Caterer · Sample", "Restaurant Business · Sample", "Financial desk · Sample"]
    },
    {
      id: "regional-awards",
      edition: "Global",
      topic: "People",
      location: "Asia-Pacific",
      time: "3 hrs ago",
      title: "Regional awards widen the map of destination dining",
      deck: "Smaller cities are gaining visibility as guides and lists look beyond established capitals.",
      image: "./assets/vienna-kitchen.webp",
      sources: 12,
      initials: ["50", "MG", "SC"],
      brief: [
        "Recent award coverage is directing more attention toward restaurants outside traditional dining capitals.",
        "Local ingredients and distinct regional service cultures are central to the newly visible destinations.",
        "Tourism bodies increasingly treat restaurant recognition as part of broader place strategy."
      ],
      why: "Recognition can materially change travel patterns and restaurant demand. It also raises questions about whether local infrastructure and staffing can absorb sudden global attention.",
      sourceNames: ["Awards body · Sample", "Michelin Guide · Sample", "Regional culture desk · Sample"]
    },
    {
      id: "cocoa-transparency",
      edition: "Global",
      topic: "Food & Wine",
      location: "Global",
      time: "4 hrs ago",
      title: "Pastry kitchens ask harder questions about cocoa",
      deck: "Traceability, flavour and price volatility are changing how chefs specify chocolate.",
      image: "./assets/vienna-bakery.webp",
      sources: 9,
      initials: ["FC", "P", "RB"],
      brief: [
        "Pastry teams are seeking more detailed origin and producer information from suppliers.",
        "Price volatility is encouraging tighter menus and more deliberate use of chocolate.",
        "Some chefs are broadening dessert programmes with grains, fruit and caramelised dairy."
      ],
      why: "Cocoa connects climate exposure, farm economics and menu pricing in a single ingredient. Better specification can improve both flavour decisions and supply-chain accountability.",
      sourceNames: ["Food climate desk · Sample", "Pastry publication · Sample", "Supplier note · Sample"]
    },
    {
      id: "restaurant-reservations",
      edition: "Global",
      topic: "Business",
      location: "New York",
      time: "6 hrs ago",
      title: "Reservation platforms compete on the guest relationship",
      deck: "Restaurants want more control over customer data, deposits and communication before the visit.",
      image: null,
      sources: 13,
      initials: ["RB", "ET", "CN"],
      brief: [
        "Operators are evaluating platforms based on guest data access and communication tools, not discovery alone.",
        "Deposits and cancellation policies continue to evolve by service style and price point.",
        "Restaurants increasingly want booking systems to connect with direct marketing and loyalty tools."
      ],
      why: "The reservation layer is becoming core customer infrastructure. Control over that relationship affects margins, repeat visits and a restaurant’s ability to communicate without relying on a marketplace.",
      sourceNames: ["Restaurant Business · Sample", "Technology desk · Sample", "Operator survey · Sample"]
    }
  ]
};

stories.austria = [
  ...stories.vienna.map((story) => ({ ...story, edition: "Austria" })),
  ...stories.austria
];
stories.vienna = [];

// An image the publisher itself put in its public feed needs no further rights
// check; anything else stays in the editorial queue.
const CLEARED_IMAGE_USAGE = new Set(["feed_provided", "permitted"]);

// A story either carries the publisher's own image or it carries none. Category
// stock art used to stand in, which made unrelated stories look alike and
// implied photography MISE does not have.
function storyImageForCluster(cluster) {
  const candidate = cluster.image_url || cluster.sources?.find((source) => source.image_url)?.image_url;
  return /^https:\/\//.test(candidate || "") ? candidate : null;
}

function storyImageAttributes(story) {
  return `src="${safeText(story.image)}" referrerpolicy="no-referrer"`;
}

// Imageless cards fall back to the topic gradient and the story's first letter,
// the same treatment the drawer uses, so the two read as one language.
function storyVisual(story, className) {
  return story.image
    ? `<div class="${className}"><img ${storyImageAttributes(story)} alt="" loading="lazy" decoding="async" /></div>`
    : `<div class="${className} feed-image-placeholder" data-topic="${safeText(story.topic)}" aria-hidden="true">${storyGlyph(story)}</div>`;
}

function inferOpeningStatus(title, summary) {
  const text = `${title || ""} ${summary || ""}`.toLowerCase();
  const foldedText = text.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  const titleText = String(title || "").toLowerCase();
  const foldedTitle = titleText.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  if (/closed|closes|closing|closure|to close|will close|geschlossen|schlie(?:ß|ss)t/.test(titleText)) return "Closed";
  if (/to open|opening soon|will open|pre-opening|scheduled|angekundigt|kommt nach|eroffnet im|eroffnet am/.test(foldedTitle)) return "Opening soon";
  if (/\bopened\b|\bopens\b|\bnow open\b|\blaunches\b|neueroffnung|neu eroffnet|eroffnete|hat eroffnet/.test(foldedTitle)) return "Newly opened";
  if (/insolven/.test(text) && !/closed|closes|closing|closure|to close|will close|geschlossen/.test(text)) return "Unconfirmed";
  if (/\bclosing\b|\bto close\b|\bwill close\b/.test(text)) return "Closed";
  if (/closed|closes|closure|insolven|geschlossen|schlie(?:ß|ss)t/.test(text)) return "Closed";
  if (/to open|opening soon|will open|pre-opening|scheduled|angekündigt|kommt nach|eröffnet im|eröffnet am/.test(text)) return "Opening soon";
  if (/rumou?r|geplant|plant ein/.test(text)) return "Unconfirmed";
  if (/\bopened\b|\bopens\b|\bnow open\b|\blaunches\b|neueroffnung|neu eroffnet|eroffnete|hat eroffnet/.test(foldedText)) return "Newly opened";
  return "Unconfirmed";
}

function relevanceScore(story) {
  const ageHours = Math.max(0, (Date.now() - new Date(story.publishedAt || 0).getTime()) / 36e5);
  const freshness = Math.max(0, 80 - ageHours / 3);
  const local = /vienna|wien/i.test(story.location) ? 48 : story.edition === "Austria" ? 34 : 12;
  const corroboration = Math.min(30, (story.independentSources || 0) * 12 + Math.max(0, story.sources - 1) * 4);
  const business = story.topic === "Business" ? 24 : 0;
  const industryEvidence = `${story.title || ""} ${story.summary || story.deck || ""}`;
  const operatorImpact = /cost|price|inflation|wage|collective agreement|labour|labor|tax|insolven|bankrupt|revenue|profit|investment|supplier|wholesale|regulation|tourism|hotel|group|chain|franchise|company|market|export|import|energy|rent/i.test(industryEvidence) ? 22 : 0;
  const pressPenalty = story.coveragePattern === "likely_syndicated" ? 22 : 0;
  return Math.round(freshness + local + corroboration + business + operatorImpact - pressPenalty);
}

function isNewsworthyOpening(story) {
  if (story.topic !== "Openings") return true;
  const evidence = `${story.title || ""} ${story.summary || story.deck || ""}`;
  return (story.independentSources || 0) > 1
    || (story.sources || 0) > 1
    || /beloved|iconic|landmark|institution|michelin|starred|chain|group|flagship|first in|arrives|expansion|insolven|bankrupt|hundred|decade|jobs|employees|acquisition|takeover/i.test(evidence);
}

function safeText(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function sourceInitials(name) {
  return String(name || "Source")
    .split(/\s+/)
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

function relativeTime(value) {
  const published = new Date(value);
  const elapsed = Date.now() - published.getTime();
  if (!Number.isFinite(elapsed)) return "Recently";
  if (elapsed < -60000) {
    const futureMinutes = Math.ceil(Math.abs(elapsed) / 60000);
    if (futureMinutes < 60) return `in ${futureMinutes} min`;
    const futureHours = Math.ceil(futureMinutes / 60);
    if (futureHours < 24) return `in ${futureHours} hr${futureHours === 1 ? "" : "s"}`;
    const futureDays = Math.ceil(futureHours / 24);
    return `in ${futureDays} day${futureDays === 1 ? "" : "s"}`;
  }
  const minutes = Math.max(1, Math.floor(elapsed / 60000));
  if (minutes < 60) return `${minutes} min ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} hr${hours === 1 ? "" : "s"} ago`;
  const days = Math.floor(hours / 24);
  return `${days} day${days === 1 ? "" : "s"} ago`;
}

function renderPipelineHealth() {
  const details = document.querySelector("#data-health");
  const summary = document.querySelector("#data-health-summary");
  const panel = document.querySelector("#data-health-panel");
  const payload = window.MISE_UPDATE_STATUS;
  if (!details || !summary || !panel) return;

  if (!payload?.stages?.length) {
    details.dataset.status = "unknown";
    summary.textContent = "Status unavailable";
    panel.innerHTML = `<p class="data-health-empty">Run the data refresh to create a health report.</p>`;
    return;
  }

  const status = ["current", "partial", "failed"].includes(payload.overall_status)
    ? payload.overall_status
    : "unknown";
  details.dataset.status = status;
  summary.textContent = status === "current"
    ? "All data current"
    : status === "partial"
      ? `${payload.issue_count || 1} data issue${payload.issue_count === 1 ? "" : "s"}`
      : "Refresh needs attention";
  const statusLabels = { current: "Current", partial: "Partial", failed: "Failed", skipped: "Skipped" };
  panel.innerHTML = `
    <div class="data-health-heading">
      <div><p class="eyebrow">DATA DESK</p><strong>${safeText(summary.textContent)}</strong></div>
      <time datetime="${safeText(payload.generated_at)}">Updated ${relativeTime(payload.generated_at)}</time>
    </div>
    <div class="data-health-stages">
      ${payload.stages.map((stage) => `
        <div class="data-health-stage" data-status="${safeText(stage.status)}">
          <span class="stage-dot" aria-hidden="true"></span>
          <div><strong>${safeText(stage.label)}</strong><small>${safeText(stage.summary)}</small></div>
          <em>${statusLabels[stage.status] || "Unknown"}</em>
        </div>`).join("")}
    </div>
    <p class="data-health-note">A partial refresh keeps the last verified cached value instead of inventing a replacement.</p>`;
}

function storyTopic(cluster) {
  const evidence = `${cluster.title || ""} ${cluster.summary || ""}`.toLowerCase();
  const directOpening = /\b(neueröffnung|eröffnet|neu in|neues lokal|neues restaurant|opening soon|opens|opened|new restaurant|new café|new cafe|new bar|schließt|geschlossen|closes|closure)\b/i;
  const venueLaunch = /\b(launches|startet|eröffnung)\b.{0,70}\b(restaurant|café|cafe|bar|bistro|venue|lokal|gastronomie|hotel)\b|\b(restaurant|café|cafe|bar|bistro|venue|lokal|gastronomie|hotel)\b.{0,70}\b(launches|startet|eröffnung)\b/i;
  if (directOpening.test(evidence) || venueLaunch.test(evidence)) return "Openings";
  if (/insolven|bankrupt|umsatz|revenue|gewinn|profit|verlust|loss|übernahme|acquisition|fusion|merger|invest|expan|franchise|kette|chain|gruppe|group|unternehmen|company|markt|market|preis|price|kosten|cost|miete|rent|steuer|tax|lohn|wage|kollektivvertrag|collective agreement|personal|staffing|arbeitsmarkt|labour|labor|tourismus|tourism|hotellerie|wholesale|supplier|lieferant/.test(evidence)) return "Business";
  if (/nachhalt|sustainab|klima|climate|food waste|lebensmittelverschwendung|mehrweg|reusable|regional sourcing/.test(evidence)) return "Sustainability";
  if (/ernennt|appointed|appoints|new chef|neuer küchenchef|geschäftsführer|managing director|ceo|personalie|joins|verlässt|departs/.test(evidence)) return "People";
  return cluster.topic || "Restaurants";
}

// Austrian reporting is German and stays German. Nothing is translated for
// display, so no story waits on a model to become visible and the words on the
// tile are the publisher's own.
const VIENNA_PATTERN = /\bwien\b|\bwiener\b|vienna|döbling|neubau|alsergrund|leopoldstadt|josefstadt|favoriten|hietzing|währing|ottakring|meidling|donaustadt|floridsdorf|landstraße|mariahilf/i;
const REGION_PATTERNS = [
  [/salzburg/i, "Salzburg"],
  [/tirol|innsbruck/i, "Tirol"],
  [/vorarlberg|bregenz|dornbirn/i, "Vorarlberg"],
  [/steiermark|graz/i, "Steiermark"],
  [/kärnten|klagenfurt|villach/i, "Kärnten"],
  [/oberösterreich|linz|wels/i, "Oberösterreich"],
  [/niederösterreich|krems|wachau|st\. pölten/i, "Niederösterreich"],
  [/burgenland|eisenstadt/i, "Burgenland"],
];

function inferLocation(text) {
  if (VIENNA_PATTERN.test(text)) return "Vienna";
  for (const [pattern, name] of REGION_PATTERNS) {
    if (pattern.test(text)) return name;
  }
  return "Austria";
}

function liveAustriaStories() {
  const payload = window.MISE_LIVE_NEWS;
  const clusters = payload?.clusters;
  if (!Array.isArray(clusters)) return [];

  return clusters
    .filter((cluster) => cluster.edition === "austria")
    .map((cluster) => {
      const sources = (cluster.sources || [])
        .filter((source) => /^https:\/\//.test(source.url || ""))
        .filter((source, index, all) => all.findIndex((candidate) => candidate.source_name === source.source_name) === index);
      const lead = sources[0];
      if (!lead) return null;
      const topic = storyTopic(cluster);
      const sourceNames = sources.map((source) => safeText(source.source_name));
      const excerpt = cluster.summary || `Meldung von ${lead.source_name}.`;
      return {
        id: `live-at-${cluster.id}`,
        edition: "Austria",
        topic,
        language: cluster.language || "de",
        location: inferLocation(`${cluster.title || ""} ${cluster.summary || ""}`),
        time: relativeTime(cluster.published_at),
        title: safeText(cluster.title),
        deck: safeText(excerpt),
        summary: safeText(excerpt),
        image: storyImageForCluster(cluster),
        imageCandidate: cluster.image_url || null,
        imageUsage: cluster.image_usage || "review_required",
      imageFromFeed: CLEARED_IMAGE_USAGE.has(cluster.image_usage),
        sources: cluster.source_count || sources.length,
        initials: sourceNames.map(sourceInitials),
        sourceNames,
        sourceLinks: sources.map((source) => ({
          name: safeText(source.source_name),
          title: safeText(source.title),
          url: source.url,
          initial: sourceInitials(source.source_name),
          role: source.corroboration_role || "independent_editorial",
          sourceType: source.source_type || "publisher"
        })),
        brief: [],
        briefType: "source_excerpt",
        clusterConfidence: cluster.cluster_confidence,
        independentSources: cluster.independent_source_count || 0,
        coveragePattern: cluster.coverage_pattern || "single_source",
        isCluster: (cluster.source_count || sources.length) > 1,
        isLive: true,
        isTranslated: false,
        summaryProvenance: "source_original",
        reviewStatus: cluster.review_status || "source_metadata_only",
        openingStatus: topic === "Openings" ? inferOpeningStatus(cluster.title, cluster.summary) : null,
        publishedAt: cluster.published_at,
        url: lead.url
      };
    })
    .filter(Boolean);
}

function liveGlobalStories() {
  const payload = window.MISE_LIVE_NEWS;
  const clusters = payload?.clusters;
  if (!Array.isArray(clusters)) return [];

  return clusters
    // Every language the collector holds, each shown as published.
    .filter((cluster) => cluster.edition === "global")
    .map((cluster) => {
      const sources = (cluster.sources || [])
        .filter((source) => /^https:\/\//.test(source.url || ""))
        .filter((source, index, all) => all.findIndex((candidate) => candidate.source_name === source.source_name) === index);
      const lead = sources[0];
      if (!lead) return null;
      const topic = storyTopic(cluster);
      const sourceNames = sources.map((source) => safeText(source.source_name));
      const initials = sourceNames.map(sourceInitials);
      return {
      id: `live-${cluster.id}`,
      edition: "Global",
      topic,
      language: cluster.language || "en",
      location: lead.country === "US" ? "United States" : lead.country || "Global",
      time: relativeTime(cluster.published_at),
      title: safeText(cluster.title),
      deck: safeText(cluster.summary || `Latest reporting from ${lead.source_name}.`),
      summary: safeText(cluster.summary || `Latest reporting from ${lead.source_name}.`),
      image: storyImageForCluster(cluster),
      imageCandidate: cluster.image_url || null,
      imageUsage: cluster.image_usage || "review_required",
      imageFromFeed: CLEARED_IMAGE_USAGE.has(cluster.image_usage),
      sources: cluster.source_count || sources.length,
      initials,
      sourceNames,
      sourceLinks: sources.map((source) => ({
        name: safeText(source.source_name),
        title: safeText(source.title),
        url: source.url,
        initial: sourceInitials(source.source_name),
        role: source.corroboration_role || "independent_editorial",
        sourceType: source.source_type || "publisher"
      })),
      brief: (cluster.brief?.bullets || []).map((bullet) => safeText(bullet.text)),
      briefType: cluster.brief?.type,
      clusterConfidence: cluster.cluster_confidence,
      independentSources: cluster.independent_source_count || 0,
      coveragePattern: cluster.coverage_pattern || "single_source",
      isCluster: (cluster.source_count || sources.length) > 1,
      isLive: true,
      isTranslated: false,
      summaryProvenance: "source_original",
      reviewStatus: cluster.review_status || cluster.brief?.review_status || "source_metadata_only",
      openingStatus: topic === "Openings" ? inferOpeningStatus(cluster.title, cluster.summary) : null,
      publishedAt: cluster.published_at,
      url: lead.url
    };
    })
    .filter(Boolean);
}

const liveAustrians = liveAustriaStories();
if (liveAustrians.length) {
  stories.austria = liveAustrians;
}

const liveGlobals = liveGlobalStories();
if (liveGlobals.length) stories.global = liveGlobals;

function readSavedStories() {
  try {
    const value = JSON.parse(window.localStorage.getItem("mise.savedStories") || "[]");
    if (Array.isArray(value)) {
      return { ids: new Set(value.filter((id) => typeof id === "string")), snapshots: new Map() };
    }
    const ids = Array.isArray(value?.ids) ? value.ids.filter((id) => typeof id === "string") : [];
    const snapshots = Object.entries(value?.stories || {}).filter(([, story]) => story && typeof story === "object");
    return { ids: new Set(ids), snapshots: new Map(snapshots) };
  } catch {
    return { ids: new Set(), snapshots: new Map() };
  }
}

function persistSavedStories() {
  try {
    window.localStorage.setItem("mise.savedStories", JSON.stringify({
      version: 2,
      ids: [...state.saved],
      stories: Object.fromEntries([...state.savedSnapshots].filter(([id]) => state.saved.has(id)))
    }));
  } catch {
    // Browsing remains functional when storage is blocked or unavailable.
  }
}

const savedStore = readSavedStories();
const state = {
  page: "news",
  section: "austria",
  newsSection: "austria",
  topic: "All",
  sort: "top",
  eventFilter: "all",
  calendarMonthOffset: 0,
  trackerMonthOffset: 0,
  trackerFilter: "all",
  marketId: null,
  saved: savedStore.ids,
  savedSnapshots: savedStore.snapshots,
  visibleCount: 18
};

const availableStoryIds = new Set(allStories().map((story) => story.id));
let prunedLegacySave = false;
for (const id of [...state.saved]) {
  if (!availableStoryIds.has(id) && !state.savedSnapshots.has(id)) {
    state.saved.delete(id);
    prunedLegacySave = true;
  }
}
if (prunedLegacySave) persistSavedStories();

const heroLayout = document.querySelector("#hero-layout");
const storyFeed = document.querySelector("#story-feed");
const feedHeading = document.querySelector("#feed-heading");
const filterRow = document.querySelector("#filter-row");
const storyOverlay = document.querySelector("#story-overlay");
const drawerContent = document.querySelector("#drawer-content");
const searchOverlay = document.querySelector("#search-overlay");
const searchInput = document.querySelector("#search-input");
const searchResults = document.querySelector("#search-results");
const toast = document.querySelector("#toast");
const scrollSentinel = document.querySelector("#scroll-sentinel");
const contextPanel = document.querySelector("#context-panel");
const newsView = document.querySelector("#news-view");
const calendarView = document.querySelector("#calendar-view");
const trackerView = document.querySelector("#tracker-view");
const marketView = document.querySelector("#market-view");
const eventOverlay = document.querySelector("#event-overlay");
const eventDrawerContent = document.querySelector("#event-drawer-content");
const trackerList = document.querySelector("#tracker-list");
const marketPanel = document.querySelector("#market-panel");
const marketStrip = document.querySelector("#market-strip");
let storyReturnFocus = null;
let searchReturnFocus = null;
let eventReturnFocus = null;

const bookmarkIcon = `
  <svg aria-hidden="true" viewBox="0 0 24 24"><path d="M6.5 4.5h11v16L12 17l-5.5 3.5z"></path></svg>
`;

function allStories() {
  return [...stories.austria, ...stories.global];
}

function currentStories() {
  let items;
  if (state.section === "saved") {
    const currentById = new Map(allStories().map((story) => [story.id, story]));
    items = [...state.saved]
      .map((id) => currentById.get(id) || state.savedSnapshots.get(id))
      .filter(Boolean);
  } else if (state.section === "openings") {
    items = stories.austria.filter((story) => story.topic === "Openings");
  } else if (state.section === "review") {
    items = allStories().filter((story) => story.isLive && (
      ["automated_unreviewed", "source_metadata_only"].includes(story.reviewStatus)
      || story.coveragePattern === "likely_syndicated"
      || (story.imageCandidate && !story.imageFromFeed)
    ));
  } else {
    items = stories[state.section] || [];
  }
  if (["austria", "global"].includes(state.section)) {
    items = items.filter(isNewsworthyOpening);
  }
  return [...items].sort((left, right) => state.sort === "latest"
    ? new Date(right.publishedAt || 0) - new Date(left.publishedAt || 0)
    : relevanceScore(right) - relevanceScore(left));
}

function sourceStack(story) {
  return `<span class="source-stack">${story.initials.map((initial) => `<i>${initial}</i>`).join("")}</span>`;
}

function storyMeta(story, light = false) {
  return `
    <div class="story-meta ${light ? "light" : ""}">
      ${sourceStack(story)}
      <span>${story.sources} ${story.sources === 1 ? "source" : "sources"}</span><span>·</span><span>${story.time}</span>
    </div>
  `;
}

function trackerEvidence(story) {
  const sourceLinks = story.sourceLinks || [];
  const roles = sourceLinks.map((source) => source.role || "independent_editorial");
  if (roles.some((role) => /social|community/.test(role))) {
    return { label: "Social post", className: "social" };
  }
  if (sourceLinks.length && sourceLinks.every((source) => source.sourceType === "official" || source.role === "official_primary")) {
    return { label: "Official record", className: "first-party" };
  }
  if (roles.length && roles.every((role) => /first_party|official_first_party/.test(role))) {
    return { label: "First-party announcement", className: "first-party" };
  }
  if (roles.length && roles.every((role) => role === "press_release")) {
    return { label: "Press release", className: "press-release" };
  }
  if ((story.independentSources || 0) > 1) {
    return { label: "Corroborated reporting", className: "corroborated" };
  }
  return { label: "Publisher report", className: "reporting" };
}

function saveButton(story, className) {
  const saved = state.saved.has(story.id);
  return `<button class="${className} ${saved ? "saved" : ""}" data-save="${story.id}" type="button" aria-label="${saved ? "Remove from saved stories" : "Save story"}">${bookmarkIcon}</button>`;
}

function selectDailyBriefing(items, limit = 5) {
  if (!items.length) return [];
  const selected = [items[0]];
  const selectedIds = new Set([items[0].id]);
  const usedTopics = new Set([items[0].topic]);

  for (const story of items.slice(1)) {
    if (selected.length >= limit) break;
    if (!usedTopics.has(story.topic)) {
      selected.push(story);
      selectedIds.add(story.id);
      usedTopics.add(story.topic);
    }
  }
  for (const story of items.slice(1)) {
    if (selected.length >= limit) break;
    if (!selectedIds.has(story.id)) {
      selected.push(story);
      selectedIds.add(story.id);
    }
  }
  return selected;
}

function storyGlyph(story) {
  const match = String(story.title || "").match(/[0-9A-Za-zÀ-ÖØ-öø-ÿ]/);
  return (match ? match[0] : "M").toUpperCase();
}

function storyByline(story) {
  const source = (story.sourceNames || [])[0] || "MISE desk";
  // The feed carries several languages side by side, so each item says which
  // one it is rather than leaving the reader to work it out from the headline.
  const language = story.language ? `<i>${safeText(story.language.toUpperCase())}</i>` : "";
  return `<div class="feed-byline">${language}${source} · ${story.time}</div>`;
}

function briefingLeadCard(story) {
  return `
    <article class="briefing-lead" data-story="${story.id}" tabindex="0" aria-label="Read lead briefing: ${story.title}">
      ${storyVisual(story, "briefing-visual")}
      ${saveButton(story, "hero-save")}
      <div class="briefing-lead-copy">
        <div class="briefing-label">${story.topic} · ${story.location}</div>
        ${story.openingStatus ? `<span class="status-badge" data-status="${story.openingStatus}">${story.openingStatus}</span>` : ""}
        <h2>${story.title}</h2>
        <p>${story.summary || story.deck}</p>
        ${storyMeta(story, true)}
      </div>
    </article>`;
}

function briefingSecondaryCard(story) {
  return `
    <article class="briefing-secondary" data-story="${story.id}" tabindex="0" aria-label="Read briefing: ${story.title}">
      ${storyVisual(story, "briefing-visual")}
      ${saveButton(story, "briefing-save")}
      <div class="briefing-secondary-copy">
        <span class="feed-topic" data-topic="${story.topic}">${story.topic} · ${story.location}</span>
        <h3>${story.title}</h3>
      </div>
    </article>`;
}

// The desk page: photo-led stories carry the visual weight and imageless items
// run as briefs, the way a trade paper sets dense text items beside its picture
// stories. Two rhythms alternate so the feature does not land on a fixed beat.
const FEED_RHYTHMS = [
  ["feature", "standard", "standard", "brief", "brief", "brief", "standard", "standard", "standard", "standard"],
  ["standard", "standard", "brief", "brief", "brief", "feature", "standard", "standard", "standard", "standard"],
];

function composeFeed(items) {
  const illustrated = items.filter((story) => story.image);
  const briefs = items.filter((story) => !story.image);
  const laid = [];
  let cycle = 0;
  let nextIllustrated = 0;
  let nextBrief = 0;

  while (nextIllustrated < illustrated.length || nextBrief < briefs.length) {
    for (const role of FEED_RHYTHMS[cycle % FEED_RHYTHMS.length]) {
      // Either queue may empty first, so each role falls back to the other
      // rather than leaving a hole in the grid.
      if (role === "brief") {
        if (nextBrief < briefs.length) laid.push({ story: briefs[nextBrief++], role: "brief" });
        else if (nextIllustrated < illustrated.length) laid.push({ story: illustrated[nextIllustrated++], role: "standard" });
      } else if (nextIllustrated < illustrated.length) {
        laid.push({ story: illustrated[nextIllustrated++], role });
      } else if (nextBrief < briefs.length) {
        laid.push({ story: briefs[nextBrief++], role: "brief" });
      }
    }
    cycle += 1;
  }
  return laid;
}

function feedCard({ story, role }) {
  const kicker = `<span class="feed-topic" data-topic="${story.topic}">${story.topic} · ${story.location}</span>`;
  const status = story.openingStatus
    ? `<span class="status-badge" data-status="${story.openingStatus}">${story.openingStatus}</span>`
    : "";

  if (role === "brief") {
    return `
      <article class="feed-story feed-story--brief" data-story="${story.id}" data-topic="${safeText(story.topic)}" tabindex="0" aria-label="Read ${story.title}">
        <div class="feed-copy">
          ${kicker}
          ${status}
          <h3>${story.title}</h3>
          ${storyByline(story)}
        </div>
      </article>`;
  }

  return `
    <article class="feed-story feed-story--${role}" data-story="${story.id}" tabindex="0" aria-label="Read ${story.title}">
      ${storyVisual(story, "feed-image")}
      <div class="feed-copy">
        ${kicker}
        ${status}
        <h3>${story.title}</h3>
        <p>${story.summary || story.deck}</p>
        ${storyByline(story)}
      </div>
      ${saveButton(story, "feed-save")}
    </article>
  `;
}

function greetingForNow() {
  const hour = new Date().getHours();
  if (hour < 12) return "Good morning.";
  if (hour < 18) return "Good afternoon.";
  return "Good evening.";
}

function marketSparkline(history, direction) {
  const values = (history || []).map((item) => Number(item.value)).filter(Number.isFinite);
  if (values.length < 2) return "";
  const low = Math.min(...values);
  const high = Math.max(...values);
  const span = high - low || 1;
  const step = 100 / (values.length - 1);
  const points = values
    .map((value, index) => `${(index * step).toFixed(2)},${(24 - ((value - low) / span) * 22).toFixed(2)}`)
    .join(" ");
  const stroke = direction === "up" ? "#7db98a" : direction === "down" ? "#e0765f" : "#9a978a";
  return `
    <svg viewBox="0 0 100 26" preserveAspectRatio="none" aria-hidden="true">
      <polygon points="0,26 ${points} 100,26" fill="${stroke}" fill-opacity="0.13"></polygon>
      <polyline points="${points}" stroke="${stroke}"></polyline>
    </svg>`;
}

function marketScopeGroup(scope) {
  const label = String(scope || "");
  if (label.startsWith("Austria")) return "Austria";
  if (label.startsWith("European Union")) return "European Union";
  return "Global";
}

function renderMarkets() {
  if (!marketPanel || !marketStrip) return;
  const payload = window.MISE_MARKETS;
  const items = payload?.benchmarks || [];
  marketPanel.hidden = !items.length;
  if (!items.length) return;

  const groups = new Map([["Austria", []], ["European Union", []], ["Global", []]]);
  items.forEach((item) => groups.get(marketScopeGroup(item.scope)).push(item));

  marketStrip.innerHTML = [...groups.entries()]
    .filter(([, groupItems]) => groupItems.length)
    .map(([groupLabel, groupItems]) => `
      <div class="market-group">
        <h4 class="market-group-heading">${safeText(groupLabel)}</h4>
        ${groupItems.map((item) => {
          const change = Number(item.change_pct);
          const direction = change > 0 ? "up" : change < 0 ? "down" : "flat";
          const changeLabel = Number.isFinite(change)
            ? `${change > 0 ? "+" : ""}${change.toFixed(1)}%`
            : "No comparison";
          const value = new Intl.NumberFormat("en-GB", {
            minimumFractionDigits: item.display_decimals || 0,
            maximumFractionDigits: item.display_decimals || 0
          }).format(Number(item.value));
          return `
            <button class="market-row" data-market="${safeText(item.id)}" type="button" aria-label="View market detail for ${safeText(item.label)}">
              <span class="market-row-name">${safeText(item.label)}</span>
              <span class="market-row-value">${value}<span>${safeText(item.unit)}</span></span>
              <span class="market-row-trend">
                ${marketSparkline(item.history, direction)}
                <span class="market-row-change ${direction}">${changeLabel}${item.stale ? " · stale" : ""}</span>
              </span>
            </button>`;
        }).join("")}
      </div>`)
    .join("");

  document.querySelector("#market-status").textContent = "Wholesale & commodity watch · no AI";
  const updated = payload.generated_at
    ? new Intl.DateTimeFormat("en-GB", { day: "numeric", month: "short" }).format(new Date(payload.generated_at))
    : "recently";
  document.querySelector("#market-methodology").textContent = `${items.length} official reference series · Updated ${updated}`;
  document.querySelectorAll("[data-market]").forEach((button) => {
    button.addEventListener("click", () => {
      state.marketId = button.dataset.market;
      switchPage("market");
    });
  });
}

function marketDetailChart(history) {
  const points = (history || []).map((item) => ({ date: item.date, value: Number(item.value) })).filter((item) => Number.isFinite(item.value));
  if (points.length < 2) return `<div class="market-chart-empty">Not enough observations for a chart.</div>`;
  const width = 760;
  const height = 280;
  const padding = 26;
  const values = points.map((item) => item.value);
  const low = Math.min(...values);
  const high = Math.max(...values);
  const span = high - low || 1;
  const coordinates = points.map((item, index) => ({
    ...item,
    x: padding + (index / (points.length - 1)) * (width - padding * 2),
    y: height - padding - ((item.value - low) / span) * (height - padding * 2)
  }));
  const line = coordinates.map((point) => `${point.x.toFixed(1)},${point.y.toFixed(1)}`).join(" ");
  const area = `${padding},${height - padding} ${line} ${width - padding},${height - padding}`;
  const first = points[0];
  const last = points.at(-1);
  return `
    <div class="market-detail-chart">
      <svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Price history from ${safeText(first.date)} to ${safeText(last.date)}">
        <line x1="${padding}" y1="${padding}" x2="${width - padding}" y2="${padding}"></line>
        <line x1="${padding}" y1="${height - padding}" x2="${width - padding}" y2="${height - padding}"></line>
        <polygon points="${area}"></polygon>
        <polyline points="${line}"></polyline>
        ${coordinates.map((point) => `<circle cx="${point.x.toFixed(1)}" cy="${point.y.toFixed(1)}" r="3"><title>${safeText(point.date)}: ${point.value}</title></circle>`).join("")}
      </svg>
      <div class="market-chart-axis"><span>${safeText(first.date)}</span><span>${safeText(points[Math.floor(points.length / 2)].date)}</span><span>${safeText(last.date)}</span></div>
    </div>`;
}

function renderMarketDetail() {
  const payload = window.MISE_MARKETS;
  const items = payload?.benchmarks || [];
  const item = items.find((candidate) => candidate.id === state.marketId) || items[0];
  const container = document.querySelector("#market-detail");
  if (!container || !item) return;
  state.marketId = item.id;
  const change = Number(item.change_pct);
  const direction = change > 0 ? "up" : change < 0 ? "down" : "flat";
  const changeLabel = Number.isFinite(change) ? `${change > 0 ? "+" : ""}${change.toFixed(1)}%` : "No comparison";
  const value = new Intl.NumberFormat("en-GB", {
    minimumFractionDigits: item.display_decimals || 0,
    maximumFractionDigits: item.display_decimals || 0
  }).format(Number(item.value));
  const period = new Intl.DateTimeFormat("en-GB", { day: "numeric", month: "long", year: "numeric" })
    .format(new Date(`${item.period}T12:00:00`));
  const historyValues = (item.history || []).map((entry) => Number(entry.value)).filter(Number.isFinite);
  const seriesHigh = historyValues.length ? Math.max(...historyValues).toLocaleString("en-GB") : "—";
  const seriesLow = historyValues.length ? Math.min(...historyValues).toLocaleString("en-GB") : "—";
  container.innerHTML = `
    <header class="market-detail-header">
      <div><p class="eyebrow">COMMODITY BOARD · ${safeText(item.scope)}</p><h2>${safeText(item.label)}</h2><p>${safeText(item.description)}</p></div>
      <div class="market-detail-quote"><strong>${value}</strong><span>${safeText(item.unit)}</span><em class="${direction}">${changeLabel} ${safeText(item.change_basis)}</em></div>
    </header>
    ${marketDetailChart(item.history)}
    <div class="market-detail-facts">
      <div><span>Series high</span><strong>${seriesHigh} ${safeText(item.unit)}</strong></div>
      <div><span>Series low</span><strong>${seriesLow} ${safeText(item.unit)}</strong></div>
      <div><span>Frequency</span><strong>${safeText(item.frequency)}${item.stale ? " · stale cached value" : ""}</strong></div>
      <div><span>Latest observation</span><strong>${period}</strong></div>
    </div>
    <div class="market-detail-footer"><p>${safeText(payload.methodology || "Directional reference benchmark, not a supplier quote.")} Source: ${safeText(item.source)}.</p><a href="${safeText(item.source_url)}" target="_blank" rel="noopener noreferrer">Open official source ↗</a></div>`;
}

// Category colours come from the Night Desk palette. The set is derived from the
// event types the pipeline actually publishes rather than a fixed list, so the
// legend can never advertise a category with no events behind it.
const EVENT_CATEGORY_COLOURS = ["#8fb3c9", "#9dd0aa", "#e8c987", "#cbb27a", "#7db98a"];

function eventCategories(events) {
  const names = [...new Set(events.map((event) => event.type).filter(Boolean))].sort();
  return new Map(names.map((name, index) => [name, EVENT_CATEGORY_COLOURS[index % EVENT_CATEGORY_COLOURS.length]]));
}

function eventsForMonth(events, year, month) {
  const monthStart = new Date(year, month, 1);
  const monthEnd = new Date(year, month + 1, 0, 23, 59, 59);
  return events.filter((event) => {
    const start = new Date(`${event.startDate}T00:00:00`);
    const end = new Date(`${event.endDate || event.startDate}T23:59:59`);
    return start <= monthEnd && end >= monthStart;
  });
}

function calendarMonthDate() {
  const base = new Date();
  base.setDate(1);
  base.setHours(0, 0, 0, 0);
  base.setMonth(base.getMonth() + state.calendarMonthOffset);
  return base;
}

function openEvent(id) {
  const payload = window.MISE_EVENTS || { events: [] };
  const event = (payload.events || []).find((item) => item.id === id);
  if (!event) return;
  eventReturnFocus = document.activeElement;
  const colours = eventCategories(payload.events || []);
  const colour = colours.get(event.type) || "var(--accent)";
  const range = new Intl.DateTimeFormat("en-GB", { day: "numeric", month: "long", year: "numeric" })
    .formatRange(new Date(`${event.startDate}T12:00:00`), new Date(`${(event.endDate || event.startDate)}T12:00:00`));
  const verified = event.verificationStatus === "stale"
    ? "Organiser page needs a recheck"
    : `Official page checked ${event.lastVerified || "recently"}`;

  eventDrawerContent.innerHTML = `
    <div class="event-drawer-body">
      <div class="event-drawer-kicker" style="color:${colour}"><span style="background:${colour}"></span>${safeText(event.type)}</div>
      <p class="eyebrow">${safeText(range)}</p>
      <h2 id="event-drawer-title">${safeText(event.title)}</h2>
      <div class="event-fact-table">
        <div><span>When</span><strong>${safeText(range)}</strong></div>
        <div><span>Where</span><strong>${safeText(event.venue)}, ${safeText(event.city)}</strong></div>
        <div><span>Audience</span><strong>${safeText(event.audience)}</strong></div>
        <div><span>Verification</span><strong>${safeText(verified)}</strong></div>
      </div>
      <h3>On the desk</h3>
      <p class="event-drawer-note">${safeText(event.summary)}</p>
      <a class="event-drawer-link" href="${safeText(event.url)}" target="_blank" rel="noopener noreferrer">${safeText(event.source)} ↗</a>
      <p class="disclosure">Dates are taken from the organiser's official page and rechecked on each refresh. Confirm with the organiser before planning or travelling.</p>
    </div>`;

  eventOverlay.classList.add("open");
  eventOverlay.setAttribute("aria-hidden", "false");
  document.body.classList.add("modal-open");
  document.querySelector("#event-close").focus();
}

function closeEvent() {
  eventOverlay.classList.remove("open");
  eventOverlay.setAttribute("aria-hidden", "true");
  document.body.classList.remove("modal-open");
  if (eventReturnFocus?.isConnected) eventReturnFocus.focus();
  eventReturnFocus = null;
}

function renderCalendar() {
  const payload = window.MISE_EVENTS || { events: [] };
  const allEvents = payload.events || [];
  const colours = eventCategories(allEvents);
  const cursor = calendarMonthDate();
  const year = cursor.getFullYear();
  const month = cursor.getMonth();
  const monthLabel = new Intl.DateTimeFormat("en-GB", { month: "long", year: "numeric" }).format(cursor);
  document.querySelector("#calendar-month-label").textContent = monthLabel;

  const visible = allEvents.filter((event) => state.eventFilter === "all" || event.type === state.eventFilter);
  const monthEvents = eventsForMonth(visible, year, month);

  document.querySelector("#calendar-filters").innerHTML = `
    <span class="calendar-filter-label">Filter</span>
    <button class="calendar-chip ${state.eventFilter === "all" ? "active" : ""}" data-event-filter="all" type="button">All</button>
    ${[...colours.entries()].map(([name, colour]) => `
      <button class="calendar-chip ${state.eventFilter === name ? "active" : ""}" data-event-filter="${safeText(name)}" type="button">
        <span style="background:${colour}"></span>${safeText(name)}
      </button>`).join("")}`;

  document.querySelector("#calendar-legend").innerHTML = [...colours.entries()].map(([name, colour]) => `
    <div class="calendar-legend-row"><span style="background:${colour}"></span>${safeText(name)}</div>`).join("")
    || `<p class="calendar-empty-note">No event categories are published yet.</p>`;

  const weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  document.querySelector("#calendar-weekdays").innerHTML = weekdays
    .map((day) => `<div>${day}</div>`).join("");

  // Monday-based grid: six fixed weeks so the layout never jumps between months.
  const firstOfMonth = new Date(year, month, 1);
  const offset = (firstOfMonth.getDay() + 6) % 7;
  const day = new Date(year, month, 1 - offset);
  const cells = [];
  for (let index = 0; index < 42; index += 1) {
    const inMonth = day.getMonth() === month;
    const isWeekend = day.getDay() === 0 || day.getDay() === 6;
    const dayEvents = inMonth
      ? monthEvents.filter((event) => {
          const start = new Date(`${event.startDate}T00:00:00`);
          const end = new Date(`${event.endDate || event.startDate}T23:59:59`);
          return day >= start && day <= end;
        })
      : [];
    cells.push(`
      <div class="calendar-cell ${inMonth ? "" : "outside"} ${isWeekend ? "weekend" : ""}">
        <span class="calendar-day">${day.getDate()}</span>
        <div class="calendar-cell-events">
          ${dayEvents.map((event) => `
            <button class="calendar-event-chip" data-event="${safeText(event.id)}" type="button" title="${safeText(event.title)}">
              <span style="background:${colours.get(event.type) || "var(--accent)"}"></span>${safeText(event.title)}
            </button>`).join("")}
        </div>
      </div>`);
    day.setDate(day.getDate() + 1);
  }
  document.querySelector("#calendar-grid").innerHTML = cells.join("");

  const agenda = [...monthEvents].sort((left, right) => left.startDate.localeCompare(right.startDate)).slice(0, 8);
  document.querySelector("#calendar-agenda").innerHTML = agenda.length
    ? agenda.map((event) => {
        const start = new Date(`${event.startDate}T12:00:00`);
        return `
          <button class="calendar-agenda-row" data-event="${safeText(event.id)}" type="button">
            <span class="calendar-agenda-date">
              <i>${new Intl.DateTimeFormat("en-GB", { weekday: "short" }).format(start)}</i>
              <b>${start.getDate()}</b>
            </span>
            <span class="calendar-agenda-copy">
              <i style="color:${colours.get(event.type) || "var(--accent)"}"><span style="background:${colours.get(event.type) || "var(--accent)"}"></span>${safeText(event.type)}</i>
              <strong>${safeText(event.title)}</strong>
              <small>${safeText(event.venue)}, ${safeText(event.city)}</small>
            </span>
          </button>`;
      }).join("")
    : `<p class="calendar-empty-note">No dated items logged for ${monthLabel} yet. The desk is still filing this month.</p>`;

  const checkedAt = payload.checkedAt
    ? new Intl.DateTimeFormat("en-GB", { day: "numeric", month: "long", year: "numeric" })
      .format(new Date(`${payload.checkedAt}T12:00:00`))
    : "not recorded";
  const reviewCount = payload.reviewCandidateCount || 0;
  document.querySelector("#event-data-note").textContent = `${allEvents.length} events checked against official organizer pages on ${checkedAt} · ${reviewCount} feed-discovered ${reviewCount === 1 ? "lead" : "leads"} awaiting organizer verification · 0 AI requests. Always confirm details before travelling.`;

  document.querySelectorAll("[data-event]").forEach((button) => {
    button.addEventListener("click", () => openEvent(button.dataset.event));
  });
  document.querySelectorAll("[data-event-filter]").forEach((button) => {
    button.addEventListener("click", () => {
      state.eventFilter = button.dataset.eventFilter;
      renderCalendar();
    });
  });
}

function startOfMonth(date = new Date()) {
  const result = new Date(date);
  result.setDate(1);
  result.setHours(0, 0, 0, 0);
  return result;
}

function trackerThemes() {
  const signals = window.MISE_TRENDS?.signals || [];
  if (!signals.length) return "";
  const peak = Math.max(...signals.map((signal) => Number(signal.current_share_pct) || 0), 1);
  return signals.map((signal) => {
    const delta = Number(signal.coverage_delta_pp);
    const direction = delta >= 3 ? "rising" : delta <= -3 ? "cooling" : "steady";
    const deltaLabel = Number.isFinite(delta)
      ? `${delta > 0 ? "+" : delta < 0 ? "−" : ""}${Math.abs(delta).toFixed(1)}pp`
      : "—";
    const share = Number(signal.current_share_pct) || 0;
    return `
      <div class="tracker-theme">
        <div class="tracker-theme-top">
          <span>${safeText(signal.label)}</span>
          <span><b>${share.toFixed(1)}%</b><i class="${direction}">${deltaLabel}</i></span>
        </div>
        <div class="tracker-theme-bar"><i class="${direction}" style="width:${Math.max(2, Math.round((share / peak) * 100))}%"></i></div>
      </div>`;
  }).join("");
}

function trackerMovers() {
  const benchmarks = window.MISE_MARKETS?.benchmarks || [];
  if (!benchmarks.length) return "";
  return [...benchmarks]
    .sort((left, right) => Math.abs(Number(right.change_pct) || 0) - Math.abs(Number(left.change_pct) || 0))
    .slice(0, 6)
    .map((item) => {
      const change = Number(item.change_pct);
      const direction = change > 0 ? "up" : change < 0 ? "down" : "flat";
      const changeLabel = Number.isFinite(change) ? `${change > 0 ? "+" : ""}${change.toFixed(1)}%` : "—";
      const value = new Intl.NumberFormat("en-GB", {
        minimumFractionDigits: item.display_decimals || 0,
        maximumFractionDigits: item.display_decimals || 0
      }).format(Number(item.value));
      return `
        <div class="tracker-mover">
          <span>${safeText(item.label)} <i>${safeText(item.unit)}</i></span>
          <span><b>${value}</b><i class="${direction}">${changeLabel}</i></span>
        </div>`;
    }).join("");
}

function renderTracker() {
  const monthStart = startOfMonth();
  monthStart.setMonth(monthStart.getMonth() - state.trackerMonthOffset);
  const monthEnd = new Date(monthStart);
  monthEnd.setMonth(monthEnd.getMonth() + 1);
  monthEnd.setMilliseconds(-1);
  const monthItems = stories.austria
    .filter((story) => story.topic === "Openings")
    .filter((story) => {
      const published = new Date(story.publishedAt || 0);
      return published >= monthStart && published <= monthEnd;
    })
    .sort((left, right) => new Date(right.publishedAt || 0) - new Date(left.publishedAt || 0));
  const statuses = monthItems.reduce((counts, story) => {
    counts[story.openingStatus || "Unconfirmed"] = (counts[story.openingStatus || "Unconfirmed"] || 0) + 1;
    return counts;
  }, {});
  const items = state.trackerFilter === "all"
    ? monthItems
    : monthItems.filter((story) => (story.openingStatus || "Unconfirmed") === state.trackerFilter);
  const monthLabel = new Intl.DateTimeFormat("en-GB", { month: "long", year: "numeric" }).format(monthStart);

  document.querySelector("#tracker-month-label").textContent = monthLabel;
  document.querySelector("#tracker-record-title").textContent = `Reported during ${monthLabel}`;
  document.querySelector("#tracker-stat-band").innerHTML = ["Newly opened", "Opening soon", "Closed", "Unconfirmed"]
    .map((status) => `
      <div class="tracker-stat">
        <p>${status}</p>
        <strong>${statuses[status] || 0}</strong>
        <small>${monthItems.length ? Math.round(((statuses[status] || 0) / monthItems.length) * 100) : 0}% of the month</small>
      </div>`).join("");

  document.querySelector("#tracker-themes").innerHTML = trackerThemes()
    || `<p class="calendar-empty-note">No trend signals are published yet.</p>`;
  document.querySelector("#tracker-movers").innerHTML = trackerMovers()
    || `<p class="calendar-empty-note">No benchmark series are published yet.</p>`;
  const basis = window.MISE_MARKETS?.benchmarks?.[0]?.change_basis;
  if (basis) document.querySelector("#tracker-movers-basis").textContent = basis;

  document.querySelectorAll("[data-tracker-filter]").forEach((button) => {
    button.classList.toggle("active", button.dataset.trackerFilter === state.trackerFilter);
  });

  trackerList.innerHTML = items.length ? items.map((story) => {
    const date = new Date(story.publishedAt);
    const evidence = trackerEvidence(story);
    return `
      <article class="tracker-entry" data-story="${story.id}" tabindex="0" aria-label="Read ${story.title}">
        <time datetime="${story.publishedAt}"><span>${new Intl.DateTimeFormat("en-GB", { weekday: "short" }).format(date)}</span><strong>${new Intl.DateTimeFormat("en-GB", { day: "2-digit" }).format(date)}</strong><small>${new Intl.DateTimeFormat("en-GB", { month: "short" }).format(date)}</small></time>
        <div class="tracker-copy">
          <div><span class="feed-topic" data-topic="${story.topic}">${story.location}</span><span class="status-badge" data-status="${story.openingStatus || "Unconfirmed"}">${story.openingStatus || "Unconfirmed"}</span><span class="evidence-badge ${evidence.className}">${evidence.label}</span></div>
          <h3>${story.title}</h3>
          <p>${story.summary || story.deck}</p>
          ${storyMeta(story)}
        </div>
        ${saveButton(story, "tracker-save")}
      </article>`;
  }).join("") : `<div class="empty-state">No ${state.trackerFilter === "all" ? "opening or closure reports" : state.trackerFilter.toLowerCase() + " reports"} were published during ${monthLabel}.</div>`;
  renderSocialWatch();
  bindCards();
}

function humanizeSignalType(value) {
  return String(value || "social signal").replaceAll("_", " ");
}

function renderSocialWatch() {
  const payload = window.MISE_SOCIAL_WATCH;
  const grid = document.querySelector("#social-watch-grid");
  const status = document.querySelector("#social-watch-status");
  const note = document.querySelector("#social-watch-note");
  if (!grid || !status || !note) return;
  const channels = payload?.channels || [];
  status.textContent = `${channels.length} catalogued channels · access unverified · 0 posts retrieved`;
  grid.innerHTML = channels.length ? channels.map((channel) => {
    const link = channel.links?.[0];
    return `
      <a class="social-source-card" href="${safeText(link)}" target="_blank" rel="noopener noreferrer">
        <div><span>${safeText(channel.platform)}</span><i>${safeText(channel.region)}</i></div>
        <h3>${safeText(channel.name)}</h3>
        <p>${safeText(humanizeSignalType(channel.signal_type))}</p>
        <strong>Open channel ↗</strong>
      </a>`;
  }).join("") : `<div class="empty-state">No catalogued social channels are currently available.</div>`;
  note.textContent = "This is a source directory, not an ingested social feed. Channel access and individual posts require manual or approved-API review before anything can appear as a labelled Social post.";
}

function renderPageShell() {
  newsView.hidden = state.page !== "news";
  calendarView.hidden = state.page !== "calendar";
  trackerView.hidden = state.page !== "tracker";
  marketView.hidden = state.page !== "market";
  document.querySelectorAll("[data-page]").forEach((button) => {
    button.classList.toggle("active", button.dataset.page === state.page);
  });
  const freshness = document.querySelector("#freshness-label");
  const livePayload = window.MISE_LIVE_NEWS;
  if (state.page === "calendar") {
    document.querySelector("#section-title").textContent = "Plan what is next.";
    freshness.textContent = "Official event sources";
  } else if (state.page === "tracker") {
    document.querySelector("#section-title").textContent = "This month's movement.";
    freshness.textContent = livePayload?.generated_at ? `News updated ${relativeTime(livePayload.generated_at)}` : "Sample dataset";
  } else if (state.page === "market") {
    document.querySelector("#section-title").textContent = "Cost intelligence.";
    freshness.textContent = window.MISE_MARKETS?.generated_at ? `Markets updated ${relativeTime(window.MISE_MARKETS.generated_at)}` : "Market data unavailable";
  } else {
    document.querySelector("#section-title").textContent = state.section === "saved" ? "Saved briefings." : greetingForNow();
    freshness.textContent = livePayload?.generated_at ? `Updated ${relativeTime(livePayload.generated_at)}` : "Sample dataset";
  }
}

function render() {
  renderPipelineHealth();
  renderPageShell();
  document.querySelector("#saved-count").textContent = state.saved.size;
  if (state.page === "calendar") {
    renderCalendar();
    return;
  }
  if (state.page === "tracker") {
    renderTracker();
    return;
  }
  if (state.page === "market") {
    renderMarketDetail();
    return;
  }
  renderMarkets();
  const items = currentStories();
  const isSaved = state.section === "saved";
  const isReview = state.section === "review";

  document.querySelectorAll("[data-section]").forEach((button) => {
    button.classList.toggle("active", button.dataset.section === state.section);
  });

  const headings = {
    austria: "What Austria is talking about",
    global: "What the world is talking about",
    saved: "Your saved briefings",
    openings: "Austria opening signals",
    review: "Stories awaiting editorial review"
  };
  feedHeading.textContent = headings[state.section] || headings.austria;
  const briefingTitles = {
    austria: "Austria's top stories",
    global: "Global top stories",
    saved: "Saved top stories",
    openings: "Opening intelligence",
    review: "Editorial review briefing"
  };
  document.querySelector("#daily-briefing-title").textContent = briefingTitles[state.section] || briefingTitles.austria;

  filterRow.style.display = isSaved || isReview ? "none" : "flex";
  const livePayload = window.MISE_LIVE_NEWS;
  const globalEnglishAvailable = livePayload?.clusters?.filter((cluster) => cluster.edition === "global" && cluster.language === "en").length || liveGlobals.length;
  document.querySelector("#austria-count").textContent = stories.austria.length;
  document.querySelector("#global-count").textContent = stories.global.length;
  const freshness = document.querySelector("#freshness-label");
  if (freshness) freshness.textContent = livePayload?.generated_at
    ? `Updated ${relativeTime(livePayload.generated_at)}`
    : "Sample dataset";
  document.querySelector("#feed-status-label").textContent = state.section === "global" && liveGlobals.length
    ? `${livePayload?.source_count || "Multiple"} live feeds · ${liveGlobals.length} recent of ${globalEnglishAvailable} English stories`
    : ["austria", "openings", "review"].includes(state.section) && liveAustrians.length
      ? `${livePayload?.source_count || "Multiple"} connected feeds · ${stories.austria.length} Austria briefings including Vienna`
      : "Editorial prototype · Sample stories";

  contextPanel.hidden = !isReview;
  if (isReview) {
    const syndicated = items.filter((story) => story.coveragePattern === "likely_syndicated").length;
    const imageCandidates = items.filter((story) => story.imageCandidate && !story.imageFromFeed).length;
    contextPanel.innerHTML = `
      <div><p class="eyebrow">EDITORIAL CONTROL</p><h2>Review before trust.</h2><p>Automated translations, single-source claims and image candidates remain visibly reviewable before production publication.</p></div>
      <div class="context-stats"><span><strong>${items.length}</strong>Unreviewed</span><span><strong>${syndicated}</strong>Shared-release risk</span><span><strong>${imageCandidates}</strong>Image rights checks</span></div>`;
  }

  if (!items.length) {
    const emptyMessages = {
      saved: "No saved stories yet. Use the bookmark on any briefing to keep it here.",
      openings: "No opening or closure signals are available in the current briefing.",
      review: "No stories currently require editorial review.",
      austria: "No Austria stories are available in the current briefing.",
      global: "No global stories are available in the current briefing."
    };
    heroLayout.innerHTML = `<div class="empty-state">${emptyMessages[state.section] || "No stories are available."}</div>`;
    document.querySelector("#daily-briefing-status").textContent = "No briefing items available";
    heroLayout.style.gridTemplateColumns = "1fr";
    storyFeed.innerHTML = "";
    bindCards();
    return;
  }

  const filteredItems = items.filter((story) => state.topic === "All" || story.topic === state.topic);
  if (!filteredItems.length) {
    heroLayout.innerHTML = `<div class="empty-state">No stories match this topic in the current briefing.</div>`;
    heroLayout.style.gridTemplateColumns = "1fr";
    storyFeed.innerHTML = "";
    scrollSentinel.hidden = true;
    document.querySelector("#daily-briefing-status").textContent = "No briefing items match this topic";
    return;
  }

  heroLayout.style.gridTemplateColumns = "";
  const briefingItems = selectDailyBriefing(filteredItems, 3);
  const lead = briefingItems[0];
  const secondary = briefingItems.slice(1);
  heroLayout.innerHTML = `
    ${briefingLeadCard(lead)}
    <div class="briefing-secondary-stack">${secondary.map(briefingSecondaryCard).join("")}</div>
  `;
  const briefingSources = new Set(briefingItems.flatMap((story) => story.sourceNames || [])).size;
  document.querySelector("#daily-briefing-status").textContent = `${briefingItems.length} top stories · ${briefingSources || briefingItems.reduce((total, story) => total + story.sources, 0)} sources · ranked for industry relevance`;

  const briefingIds = new Set(briefingItems.map((story) => story.id));
  const feedItems = filteredItems.filter((story) => !briefingIds.has(story.id));
  const visibleFeedItems = feedItems.slice(0, state.visibleCount);

  storyFeed.innerHTML = visibleFeedItems.length
    ? composeFeed(visibleFeedItems).map(feedCard).join("")
    : `<div class="empty-state">No stories match this topic in the current briefing.</div>`;
  scrollSentinel.hidden = !feedItems.length || visibleFeedItems.length >= feedItems.length;
  const loadedCount = Math.min(filteredItems.length, visibleFeedItems.length + briefingItems.length);
  scrollSentinel.textContent = visibleFeedItems.length < feedItems.length
    ? `Showing ${loadedCount} of ${filteredItems.length} · loading more…`
    : `All ${filteredItems.length} stories loaded`;

  bindCards();
}

// A publisher image that fails to load degrades to the imageless treatment
// rather than to stock art, so a dead CDN link never invents a photograph.
function bindImageFallbacks(root = document) {
  root.querySelectorAll(".feed-image img, .briefing-visual img, .drawer-hero img").forEach((image) => {
    image.addEventListener("error", () => {
      const frame = image.parentElement;
      if (!frame) return;
      const card = frame.closest("[data-story]") || frame;
      const topic = card.querySelector("[data-topic]")?.dataset.topic || "";
      frame.classList.add("feed-image-placeholder");
      frame.dataset.topic = topic;
      frame.textContent = (card.querySelector("h3, h2, h4")?.textContent || "M").trim()[0].toUpperCase();
    }, { once: true });
  });
}

function bindCards() {
  bindImageFallbacks();

  document.querySelectorAll("[data-story]").forEach((card) => {
    card.addEventListener("click", () => openStory(card.dataset.story));
    card.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openStory(card.dataset.story);
      }
    });
  });

  document.querySelectorAll("[data-save]").forEach((button) => {
    button.addEventListener("click", (event) => {
      event.stopPropagation();
      toggleSaved(button.dataset.save);
    });
  });
}

function findStory(id) {
  return allStories().find((story) => story.id === id) || state.savedSnapshots.get(id);
}

function toggleSaved(id) {
  const story = findStory(id);
  if (!story) return;

  if (state.saved.has(id)) {
    state.saved.delete(id);
    state.savedSnapshots.delete(id);
    showToast("Removed from saved stories");
  } else {
    state.saved.add(id);
    state.savedSnapshots.set(id, story);
    showToast("Saved for later");
  }
  persistSavedStories();
  render();
}

function whyItMatters(story) {
  // Live stories branch on corroboration rather than generic prose (handoff §5d).
  if (story.isLive) {
    return (story.independentSources || 0) > 1
      ? `Reported independently by ${story.independentSources} outlets, so the core facts are corroborated. Still confirm dates and figures with the operator before acting.`
      : "Single-source at the time of filing. Treat the detail as provisional and verify directly before you price, staff or plan against it.";
  }
  if (story.openingStatus === "Closed") return "Closures affect neighbourhood hospitality, employment and the local competitive landscape. The status remains tied to the publisher evidence shown below.";
  if (story.topic === "Openings") return "New venues are an early signal of how Vienna and Austria’s dining landscape is changing—by neighbourhood, format and price point.";
  if (/vienna|wien/i.test(story.location)) return "This story has direct local relevance for Vienna’s hospitality community and is prioritised in the Austria edition.";
  if (story.topic === "Business") return "The development may affect operating costs, staffing, investment or competitive conditions across hospitality businesses.";
  return "MISE ranks this story using freshness, geographic relevance, source quality and corroboration signals.";
}

const LANGUAGE_NAMES = { de: "German", en: "English", fr: "French" };

function provenanceKicker(story) {
  if (story.summaryProvenance === "source_original") {
    const language = LANGUAGE_NAMES[story.language] || "the original language";
    return `Headline and standfirst exactly as the publisher filed them, in ${language}. MISE has not translated, rewritten or summarised this item.`;
  }
  if (story.summaryProvenance === "manual") {
    return "Headline and standfirst written by a MISE editor from the original German reporting.";
  }
  if (story.summaryProvenance === "ai") {
    return "Headline, standfirst and summary machine-translated from the original German source and not yet editor-reviewed.";
  }
  return "Drawn from source metadata only — no MISE summary has been written for this item yet.";
}

function openStory(id) {
  const story = findStory(id);
  if (!story) return;
  storyReturnFocus = document.activeElement;
  const placeLabel = story.location === story.edition
    ? story.edition
    : `${story.edition} · ${story.location}`;

  const liveCoverage = story.isLive
    ? story.sourceLinks.map((source) => `
      <a class="source-row" href="${source.url}" target="_blank" rel="noopener noreferrer">
        <span class="source-icon">${source.initial}</span>
        <p>${source.name}<small>${source.title}</small></p>
        <span>Read at source ↗</span>
      </a>
    `).join("")
    : "";

  const storyDetails = story.isLive
    ? `
      <section class="ai-brief live-excerpt">
        <div class="ai-label"><span>${story.isCluster ? "✦" : "↗"}</span>${story.isCluster
          ? story.coveragePattern === "likely_syndicated"
            ? `Multi-outlet coverage · ${story.sources} outlets · likely shared release`
            : `Evidence brief · ${story.independentSources} independent of ${story.sources} sources`
          : `Publisher feed excerpt · ${LANGUAGE_NAMES[story.language] || "original language"} · no AI`}</div>
        ${story.isCluster && story.brief.length
          ? `<ul>${story.brief.map((item) => `<li>${item}</li>`).join("")}</ul>`
          : `<p>${story.deck}</p>`}
        <p class="provenance-kicker">${provenanceKicker(story)}</p>
      </section>

      <section class="drawer-section">
        <h3>Sources</h3>
        <div class="source-list">
          ${liveCoverage}
        </div>
      </section>

      <p class="disclosure">${story.isCluster
        ? story.coveragePattern === "likely_syndicated"
          ? "These outlets appear to be covering the same announcement and may rely on shared press material. MISE shows both links but does not treat repetition as independent confirmation. No article body was copied."
          : "This evidence brief uses short publisher feed excerpts. Each bullet remains traceable to the linked coverage; no article body was copied and no generative AI was used in this clustering pass."
        : "Every word above is the publisher's own feed title and excerpt, shown in the language it was filed in. MISE has not translated, summarised or copied the article body. Follow the source link for the full reporting."}</p>
    `
    : `
      <section class="ai-brief">
        <div class="ai-label"><span>✦</span>AI briefing · reviewed format</div>
        <ul>${story.brief.map((item) => `<li>${item}</li>`).join("")}</ul>
      </section>

      <section class="drawer-section">
        <h3>Sources</h3>
        <div class="source-list">
          ${story.sourceNames.map((name, index) => `
            <div class="source-row">
              <span class="source-icon">${story.initials[index % story.initials.length]}</span>
              <p>${name}<small>Representative source · Prototype</small></p>
              <span>↗</span>
            </div>
          `).join("")}
        </div>
      </section>

      <p class="disclosure">This is a sample story created to demonstrate the editorial product and interface. It is not live reporting. In production, every claim would be linked to retrieved evidence and every source row would open the original publication.</p>
    `;

  const drawerHero = story.image
    ? `<div class="drawer-hero"><img ${storyImageAttributes(story)} alt="" decoding="async" /></div>`
    : `<div class="drawer-hero feed-image-placeholder" data-topic="${safeText(story.topic)}" aria-hidden="true">${storyGlyph(story)}</div>`;

  drawerContent.innerHTML = `
    ${drawerHero}
    <div class="drawer-body">
      <span class="feed-topic" data-topic="${story.topic}">${placeLabel} · ${story.topic}</span>
      <h2 id="drawer-title">${story.title}</h2>
      <p class="drawer-deck">${story.summary || story.deck}</p>
      <div class="drawer-meta">${storyMeta(story)}</div>

      <section class="drawer-section operator-note">
        <h3>Why it matters for operators</h3>
        <p>${story.isLive ? whyItMatters(story) : story.why || whyItMatters(story)}</p>
      </section>

      ${storyDetails}
    </div>
  `;
  bindImageFallbacks(drawerContent);

  storyOverlay.classList.add("open");
  storyOverlay.setAttribute("aria-hidden", "false");
  document.body.classList.add("modal-open");
  document.querySelector("#drawer-close").focus();
}

function closeStory() {
  storyOverlay.classList.remove("open");
  storyOverlay.setAttribute("aria-hidden", "true");
  document.body.classList.remove("modal-open");
  if (storyReturnFocus?.isConnected) storyReturnFocus.focus();
  storyReturnFocus = null;
}

function switchSection(section) {
  state.page = "news";
  state.section = section;
  if (["austria", "global"].includes(section)) state.newsSection = section;
  state.topic = "All";
  state.visibleCount = 18;
  document.querySelectorAll(".filter-chip").forEach((chip) => chip.classList.toggle("active", chip.dataset.topic === "All"));
  render();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function switchPage(page) {
  state.page = page;
  if (page === "news" && !["austria", "global", "saved"].includes(state.section)) {
    state.section = state.newsSection;
  }
  state.visibleCount = 18;
  render();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function openSearch() {
  searchReturnFocus = document.activeElement;
  searchOverlay.classList.add("open");
  searchOverlay.setAttribute("aria-hidden", "false");
  document.body.classList.add("modal-open");
  searchInput.value = "";
  renderSearchResults("");
  window.setTimeout(() => searchInput.focus(), 100);
}

function closeSearch() {
  searchOverlay.classList.remove("open");
  searchOverlay.setAttribute("aria-hidden", "true");
  document.body.classList.remove("modal-open");
  if (searchReturnFocus?.isConnected) searchReturnFocus.focus();
  searchReturnFocus = null;
}

function renderSearchResults(query) {
  const term = query.trim().toLowerCase();
  const results = allStories().filter((story) => {
    const haystack = `${story.title} ${story.summary || story.deck} ${story.topic} ${story.location} ${(story.sourceNames || []).join(" ")}`.toLowerCase();
    return !term || haystack.includes(term);
  }).slice(0, 20);

  searchResults.innerHTML = results.length
    ? results.map((story) => `
      <button class="search-result" data-search-story="${story.id}" type="button">
        ${story.image ? `<img src="${story.image}" alt="" loading="lazy" decoding="async" />` : `<span class="mini-placeholder"></span>`}
        <span><strong>${story.title}</strong><small>${story.edition} · ${story.topic} · ${story.sources} ${story.sources === 1 ? "source" : "sources"}</small></span>
      </button>
    `).join("")
    : `<div class="empty-state">No briefings found.</div>`;

  document.querySelectorAll("[data-search-story]").forEach((button) => {
    button.addEventListener("click", () => {
      const id = button.dataset.searchStory;
      closeSearch();
      openStory(id);
    });
  });
}

let toastTimer;
function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => toast.classList.remove("show"), 1800);
}

function trapModalFocus(event, container) {
  const focusable = [...container.querySelectorAll(
    'a[href], button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])'
  )].filter((element) => !element.hidden && element.getClientRects().length);
  if (!focusable.length) return;
  const first = focusable[0];
  const last = focusable[focusable.length - 1];
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
}

document.querySelectorAll("[data-section]").forEach((button) => {
  button.addEventListener("click", () => switchSection(button.dataset.section));
});

document.querySelectorAll("[data-page]").forEach((button) => {
  button.addEventListener("click", () => switchPage(button.dataset.page));
});

document.querySelector("#calendar-prev").addEventListener("click", () => {
  state.calendarMonthOffset -= 1;
  renderCalendar();
});

document.querySelector("#calendar-next").addEventListener("click", () => {
  state.calendarMonthOffset += 1;
  renderCalendar();
});

document.querySelector("#event-close").addEventListener("click", closeEvent);
eventOverlay.querySelector(".overlay-backdrop").addEventListener("click", closeEvent);

// trackerMonthOffset counts backwards from the current month, so "previous"
// increases it.
document.querySelector("#tracker-prev").addEventListener("click", () => {
  state.trackerMonthOffset += 1;
  renderTracker();
});

document.querySelector("#tracker-next").addEventListener("click", () => {
  state.trackerMonthOffset -= 1;
  renderTracker();
});

document.querySelectorAll("[data-tracker-filter]").forEach((button) => {
  button.addEventListener("click", () => {
    state.trackerFilter = button.dataset.trackerFilter;
    renderTracker();
  });
});

document.querySelector(".site-header .brand").addEventListener("click", (event) => {
  event.preventDefault();
  state.section = state.newsSection;
  switchPage("news");
});

document.querySelector("#market-back").addEventListener("click", () => switchPage("news"));

document.querySelectorAll(".filter-chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    state.topic = chip.dataset.topic;
    state.visibleCount = 18;
    document.querySelectorAll(".filter-chip").forEach((item) => item.classList.toggle("active", item === chip));
    render();
  });
});

document.querySelectorAll("[data-sort]").forEach((chip) => {
  chip.addEventListener("click", () => {
    state.sort = chip.dataset.sort;
    state.visibleCount = 18;
    document.querySelectorAll("[data-sort]").forEach((item) => item.classList.toggle("active", item === chip));
    render();
  });
});

document.querySelector("#drawer-close").addEventListener("click", closeStory);
storyOverlay.querySelector(".overlay-backdrop").addEventListener("click", closeStory);
document.querySelector("#open-search").addEventListener("click", openSearch);
document.querySelector("#search-close").addEventListener("click", closeSearch);
searchOverlay.querySelector(".overlay-backdrop").addEventListener("click", closeSearch);
searchInput.addEventListener("input", (event) => renderSearchResults(event.target.value));

document.addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
    event.preventDefault();
    openSearch();
  }
  if (event.key === "Tab") {
    if (storyOverlay.classList.contains("open")) {
      trapModalFocus(event, storyOverlay.querySelector(".story-drawer"));
    } else if (eventOverlay.classList.contains("open")) {
      trapModalFocus(event, eventOverlay.querySelector(".story-drawer"));
    } else if (searchOverlay.classList.contains("open")) {
      trapModalFocus(event, searchOverlay.querySelector(".search-panel"));
    }
  }
  if (event.key === "Escape") {
    if (storyOverlay.classList.contains("open")) closeStory();
    else if (eventOverlay.classList.contains("open")) closeEvent();
    else if (searchOverlay.classList.contains("open")) closeSearch();
  }
});

const formattedDate = new Intl.DateTimeFormat("en-GB", {
  weekday: "long",
  day: "2-digit",
  month: "long",
  year: "numeric"
}).format(new Date()).toUpperCase();
document.querySelector("#today-label").textContent = formattedDate.replace(",", " ·");

const feedObserver = new IntersectionObserver((entries) => {
  if (!entries[0].isIntersecting || scrollSentinel.hidden) return;
  state.visibleCount += 18;
  render();
}, { rootMargin: "500px 0px" });
feedObserver.observe(scrollSentinel);

render();
