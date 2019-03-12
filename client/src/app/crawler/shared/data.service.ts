import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject } from 'rxjs';

@Injectable()
export class DataService {
    baseUrl = 'crawler/'
    private results = new BehaviorSubject<any>([]);
    cast = this.results.asObservable();
    private crawling = new BehaviorSubject<Boolean>(false);

    constructor(private httpClient: HttpClient) { }

    getResults() {
        return this.results;
    }

    getStatus() {
        return this.crawling;
    }

    setResults(results: any[]) {
        this.results.next(results);
    }

    crawl(url: String, depth: Number) {
        this.crawling.next(true);
        this.httpClient.post(this.baseUrl + 'crawl/', {
            url: url,
            depth: depth
        }).subscribe((response) => {
            this.crawling.next(false);
            console.log(response);
            this.results.next(response);
        }, (error) => {
            this.crawling.next(false);
            console.log(error);
            this.results.next([]);
        })
    }
}