class Settings:
    PROJECT_NAME: str = "TFF Leagues API"
    VERSION: str = "2.3.0"
    TFF_URL: str = "https://www.tff.org/default.aspx?pageID="
    HTTP_TIMEOUT: int = 10
    CACHE_EXPIRE: int = 600
    DESCRIPTION: str = "Asynchronous API for Turkish Football Leagues"

    # Single group structure (BASİT LİGLER: Tek grup yapısı)
    LEAGUES = {
        "trendyol-super-league": "198",        # Trendyol Süper Lig
        "trendyol-1-league": "142",            # Trendyol 1. Lig
        "turkcell-womens-super-league": "1000",# Turkcell Kadın Futbol Süper Ligi
        "turk-telekom-e-super-league": "1610", # Türk Telekom eSüper Lig
        "tff-futsal-league": "1640"            # Futsal Ligi
    }

    # MULTI-GROUP LEAGUES: Multiple groups/sections (ÇOKLU GRUP LİGLERİ: Çoklu grup/bölüm yapısı)
    MULTI_GROUP_LEAGUES = {
        "nesine-2-league": "976",              # Nesine 2. Lig
        "nesine-3-league": "971",              # Nesine 3. Lig
        "regional-amateur-league-bal": "1596", # Bölgesel Amatör Lig (BAL)
        "womens-1-league": "1602",             # TFF Kadınlar 1. Ligi
        "womens-2-league": "1001",             # TFF Kadınlar 2. Ligi
        "womens-3-league": "1298",             # TFF Kadınlar 3. Ligi
        "u19-paf-league": "1750",              # U19 PAF Ligi
        "u19-development-league": "1751",      # U19 Gelişim Ligi
        "u17-development-league": "1752",      # U17 Gelişim Ligi
        "u16-development-league": "1753",      # U16 Gelişim Ligi
        "u15-development-league": "1754",      # U15 Gelişim Ligi
        "u14-development-league": "1755",      # U14 Gelişim Ligi
        "u13-development-league": "1762",      # U13 Gelişim Ligi
        "youth-infrastructure-development": "1494" # Futbol Altyapı Gelişim Ligi
    }

settings = Settings()