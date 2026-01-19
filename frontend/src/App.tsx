import { Link } from "react-router"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { CheckCircle2, Network, Shield, TrendingDown, Leaf, BarChart3, Zap } from "lucide-react"
import ChainViz from '@/assets/supply-chain-network-graph-visualization.jpg'

export default function App() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border/50 backdrop-blur-sm sticky top-0 z-50 bg-background/80">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center gap-3">
              <img src="https://rvce.edu.in/wp-content/uploads/2025/08/Logo-2-300x129.png" alt="RVCE Logo" className="h-10 w-10" />
              <span className="text-xl font-bold">SupplyChain AI</span>
            </div>
            <div className="flex items-center gap-3">
              <Button variant="ghost" asChild>
                <Link to="/login">Sign In</Link>
              </Button>
              <Button asChild className="bg-primary hover:bg-primary/90">
                <Link to="/signup">Sign Up</Link>
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-transparent to-accent/10 blur-3xl" />
        <div className="container relative mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-32">
          <div className="mx-auto max-w-4xl text-center">
            <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-6 text-balance">
              Transform Your Supply Chain with <span className="text-primary">AI Intelligence</span>
            </h1>
            <p className="text-lg sm:text-xl text-muted-foreground mb-8 max-w-2xl mx-auto text-balance leading-relaxed">
              Automatically map, analyze, and optimize your entire supply pipeline. Detect compliance violations,
              discover cost savings, and find sustainable alternatives—all powered by advanced AI.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Button size="lg" asChild className="bg-primary hover:bg-primary/90 text-lg px-8 h-12">
                <Link to="/signup">Get Started Free</Link>
              </Button>
              <Button size="lg" variant="outline" className="text-lg px-8 h-12 bg-transparent">
                Watch Demo
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 md:py-28 bg-secondary/30">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">Intelligent Supply Chain Analysis</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Leverage AI to gain unprecedented visibility and control over your supply chain operations
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <Card className="bg-card border-border/50 hover:border-primary/50 transition-colors">
              <CardContent className="p-6">
                <div className="mb-4 p-3 bg-primary/10 rounded-lg w-fit">
                  <Network className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Automatic Mapping</h3>
                <p className="text-muted-foreground leading-relaxed">
                  AI-powered graph generation creates a comprehensive visual map of your entire supply chain network in
                  minutes.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-card border-border/50 hover:border-primary/50 transition-colors">
              <CardContent className="p-6">
                <div className="mb-4 p-3 bg-accent/10 rounded-lg w-fit">
                  <Shield className="h-6 w-6 text-accent" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Compliance Detection</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Continuously monitor and identify compliance violations across regulations, certifications, and
                  industry standards.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-card border-border/50 hover:border-primary/50 transition-colors">
              <CardContent className="p-6">
                <div className="mb-4 p-3 bg-primary/10 rounded-lg w-fit">
                  <TrendingDown className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Cost Optimization</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Discover cheaper alternatives and cost-saving opportunities through intelligent supplier and route
                  analysis.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-card border-border/50 hover:border-primary/50 transition-colors">
              <CardContent className="p-6">
                <div className="mb-4 p-3 bg-accent/10 rounded-lg w-fit">
                  <Leaf className="h-6 w-6 text-accent" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Sustainability Insights</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Identify eco-friendly routes and suppliers to reduce your carbon footprint and meet sustainability
                  goals.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-card border-border/50 hover:border-primary/50 transition-colors">
              <CardContent className="p-6">
                <div className="mb-4 p-3 bg-primary/10 rounded-lg w-fit">
                  <BarChart3 className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Deep Analytics</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Research every component of your supply chain with detailed reports and actionable recommendations.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-card border-border/50 hover:border-primary/50 transition-colors">
              <CardContent className="p-6">
                <div className="mb-4 p-3 bg-accent/10 rounded-lg w-fit">
                  <Zap className="h-6 w-6 text-accent" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Real-time Monitoring</h3>
                <p className="text-muted-foreground leading-relaxed">
                  Stay updated with continuous monitoring and instant alerts for changes in your supply chain ecosystem.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 md:py-28">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-4">How It Works</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">Get started in three simple steps</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="text-center">
              <div className="mb-4 mx-auto w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
                <span className="text-2xl font-bold text-primary">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Describe Your Pipeline</h3>
              <p className="text-muted-foreground leading-relaxed">
                Sign up and describe your supply chain, services, and suppliers through our intuitive interface.
              </p>
            </div>

            <div className="text-center">
              <div className="mb-4 mx-auto w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
                <span className="text-2xl font-bold text-primary">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">AI Generates Graph</h3>
              <p className="text-muted-foreground leading-relaxed">
                Our AI agent automatically creates a comprehensive visual map of your entire supply network.
              </p>
            </div>

            <div className="text-center">
              <div className="mb-4 mx-auto w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
                <span className="text-2xl font-bold text-primary">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Get Insights</h3>
              <p className="text-muted-foreground leading-relaxed">
                Receive detailed analysis on compliance, costs, sustainability, and optimization opportunities.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section className="py-20 md:py-28 bg-secondary/30">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12 items-center max-w-6xl mx-auto">
            <div>
              <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-6">Why Choose SupplyChain AI?</h2>
              <div className="space-y-4">
                <div className="flex gap-3">
                  <CheckCircle2 className="h-6 w-6 text-accent shrink-0 mt-0.5" />
                  <div>
                    <h4 className="font-semibold mb-1">Comprehensive Coverage</h4>
                    <p className="text-muted-foreground">
                      Analyze every component of your supply chain, no matter how complex.
                    </p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <CheckCircle2 className="h-6 w-6 text-accent shrink-0 mt-0.5" />
                  <div>
                    <h4 className="font-semibold mb-1">AI-Powered Insights</h4>
                    <p className="text-muted-foreground">
                      Leverage advanced machine learning for intelligent recommendations.
                    </p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <CheckCircle2 className="h-6 w-6 text-accent shrink-0 mt-0.5" />
                  <div>
                    <h4 className="font-semibold mb-1">Save Time & Money</h4>
                    <p className="text-muted-foreground">
                      Automate manual processes and discover cost-saving opportunities.
                    </p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <CheckCircle2 className="h-6 w-6 text-accent shrink-0 mt-0.5" />
                  <div>
                    <h4 className="font-semibold mb-1">Stay Compliant</h4>
                    <p className="text-muted-foreground">
                      Proactively identify and resolve compliance issues before they become problems.
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-br from-primary/30 to-accent/20 rounded-2xl blur-3xl" />
              <img
                src={ChainViz}
                alt="Supply Chain Visualization"
                className="relative rounded-2xl shadow-2xl w-full"
              />
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 md:py-28">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-6 text-balance">
              Ready to Optimize Your Supply Chain?
            </h2>
            <p className="text-lg text-muted-foreground mb-8 leading-relaxed">
              Join forward-thinking businesses that are transforming their supply chains with AI-powered intelligence.
            </p>
            <Button size="lg" asChild className="bg-primary hover:bg-primary/90 text-lg px-8 h-12">
              <Link to="/signup">Start Using Now</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/50 py-8">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center text-sm text-muted-foreground">
            <p>Credits to AIML department, created by Shashank K and Shravya S</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
